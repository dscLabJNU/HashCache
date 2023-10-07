import requests
import pandas as pd
from locust import TaskSet, task, tag
from locust.exception import RescheduleTask
from datetime import datetime, timedelta
import random
import logging
import json
import sys
sys.path.append("../")
import constant


with open(f'{constant.UTILS_DIR}/api_config.json') as f:
    api_config = json.load(f)

with open(f'{constant.UTILS_DIR}/action_api.json') as f:
    action_api = json.load(f)

STATION_DF = pd.read_csv(f'{constant.STATION_PATH}/US_to_others.csv')
OTHER_STATIONS = list(STATION_DF['to'].unique())

class SingleTask(TaskSet):
    def on_start(self):
        self.orders = []
        self.travels = []

    #################### Utils Methods Start ####################
    def pick_random_travel(self):
        # Always up-to-date
        self.travels = self.get_left_trip_tickets()

        """
        NOTE: Some travel information may be empty and
        random.choice() cannot be applied.
        """
        return random.choice(self.travels) if self.travels else []

    def pick_random_order(self):
        # Always up-to-date
        self.orders = self.query_orders_for_refresh()
        # Get a random order to pay or cancel, even if it may fail
        return random.choice(self.orders)

    def flush_action_cache(self, action):
        _, namespace, action_name = action.split("/")
        request_url = f"{constant.WHISK_APIHOST_HTTPS}/api/v1/namespaces/{namespace}/actions/{action_name}{constant.ACTION_FLUSH_SUFFIX}"
        # logging.debug(f"Request url: {request_url}")
        response = requests.get(request_url, auth=(
            constant.WHISK_USERNAME, constant.WHISK_PASSWD), verify=False)
        logging.debug(f"Flushing action: {action}: {response}")

    def general_post_action(self, action_name, params):
        api = action_api[action_name]
        logging.debug(f"invoking action {action_name} [{params}]...")
        with self.client.post(api, json=params, catch_response=True) as resp:
            if resp.status_code != 200:
                logging.error(
                    f"invoke action: {action_name} got status code={resp.status_code}, now RescheduleTask")
                self.flush_action_cache(action_name)
                raise RescheduleTask()

            resp_json = resp.json()
            logging.debug(f"===============> Invoke Result: {resp_json}")
            if 'data' not in resp_json:
                logging.error(
                    f"invoke action: {action_name} got error({resp_json}), now RescheduleTask")
                self.flush_action_cache(action_name)
                raise RescheduleTask()
            return resp_json['data']

    def general_get_action(self, action_name, api, params=None):
        logging.debug(f"invoking action {action_name}...")
        resp = self.client.get(api, json=params)
        logging.debug(f"res: {resp.json()}")
        return resp.json()['data']

    def get_random_depature_time(self):
        now = datetime.now() + timedelta(days=random.randint(0, 4))
        return now.strftime("%Y-%m-%d")

    def pick_random_contact(self):
        # Always up-to-date
        self.contacts = self.find_contacts_by_accoundId()
        return random.choice(self.contacts)
    #################### Utils Methods End ####################

    #################### APIs Start ####################

    @tag('read')
    @tag("/guest/query-orders-for-refresh")
    @task(api_config['/guest/query-orders-for-refresh']['rate'])
    def query_orders_for_refresh(self):
        action_name = '/guest/query-orders-for-refresh'
        params = api_config[action_name]['params']
        self.orders = self.general_post_action(
            action_name=action_name, params=params)
        return self.orders

    @tag('read')
    @tag("get_left_trip_tickets")
    @task(api_config['/guest/get-left-trip-tickets']['rate'])
    def get_left_trip_tickets(self):
        def place_pair():
            US_station = "United States"
            other_stations = list(OTHER_STATIONS)
            random_station = random.sample(other_stations, 1)[0]
            return [US_station, random_station]

        action_name = '/guest/get-left-trip-tickets'
        params = api_config[action_name]['params']
        # logging.debug(f"Get left trip tickets from {place_pair()[0]} to {place_pair()[1]}")

        # Update random params
        params["__post_data"] = {
            "startingPlace": place_pair()[0],
            "endPlace": place_pair()[1],
            "departure_time": self.get_random_depature_time(),
        }
        self.travels = self.general_post_action(
            action_name=action_name, params=params)
        return self.travels

    @tag("find_contacts_by_accoundId")
    @tag('read')
    @task(api_config['/guest/find-contacts-by-accountid']['rate'])
    def find_contacts_by_accoundId(self):

        action_name = '/guest/find-contacts-by-accountid'
        params = api_config[action_name]['params']

        api = action_api[action_name].replace(
            "{accountId}", params['accountId'])
        # logging.debug(f"finding contacts of accound: {params['accountId']}...")

        return self.general_get_action(api=api, action_name=action_name)

    @tag('write')
    @task(api_config['/guest/preserve-ticket']['rate'])
    def preserve_ticket(self):
        def pick_random_seat_type():
            seat_types = ["2", "3"]
            return random.choice(seat_types)

        travel = self.pick_random_travel()
        if not travel:
            logging.debug("Not travel, interrupt...")
            self.interrupt()
        action_name = '/guest/preserve-ticket'
        params = api_config[action_name]['params']
        departure_time = self.get_random_depature_time()
        contacts = self.pick_random_contact()
        trip_id = f"{travel['tripId']['type']}{travel['tripId']['number']}"
        # Update params
        params["__post_data"].update({
            "date": departure_time,
            "accountId": "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f",  # -> using default value
            "contactsId": contacts['id'],
            "tripId": trip_id,
            # 2 for 1st class seat,  3 for 2rd class seat, pick randomly
            "seatType": pick_random_seat_type(),
            "from": travel['startingStation'],
            "to": travel['terminalStation'],
            "foodType": 0  # Unknow how to get this param, using default value
        })
        return self.general_post_action(action_name=action_name, params=params)

    @tag('write')
    @task(api_config['/guest/pay-for-the-order']['rate'])
    def pay_for_the_order(self):
        order = self.pick_random_order()

        action_name = "/guest/pay-for-the-order"
        params = api_config[action_name]['params']
        params["__post_data"] = {
            "orderId": order['id'],
            'tripId': order['trainNumber'],
            'userId': order['accountId']
        }
        self.general_post_action(action_name=action_name, params=params)

    @tag('write')
    @task(api_config["/guest/cancel-ticket"]['rate'])
    def cancel_ticket(self):
        order = self.pick_random_order()

        action_name = "/guest/cancel-ticket"
        params = api_config[action_name]['params']
        params["orderId"] = order['id']
        params['loginId'] = order['accountId']

        api = action_api[action_name].replace(
            "{orderId}", params['orderId']).replace("{loginId}", params['loginId'])
        logging.debug(f"canceling order: {params['orderId']}, ")
        return self.general_get_action(api=api, action_name=action_name)

    @tag('read')
    @task(api_config["/guest/calculate-refund"]['rate'])
    def calculate_refund(self):
        order = self.pick_random_order()

        action_name = "/guest/calculate-refund"
        params = api_config[action_name]['params']
        params["orderId"] = order['id']

        api = action_api[action_name].replace("{orderId}", params['orderId'])
        logging.debug(f"calculating refund of order: {params['orderId']}")
        return self.general_get_action(api=api, action_name=action_name)
    #################### APIs End ####################
