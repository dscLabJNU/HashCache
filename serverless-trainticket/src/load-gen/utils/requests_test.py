import requests
# Ignore the verification warning
requests.packages.urllib3.disable_warnings()
from datetime import datetime, timedelta
import json
import constant
import random

with open('api_config.json') as f:
    api_config = json.load(f)

with open('action_api.json') as f:
    action_api = json.load(f)


"""
export AUTH=23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP
export APIHOST=172.10.8.101:31001

curl -k -u $AUTH "https://$APIHOST/api/v1/namespaces/_/actions/query-orders-for-refresh?blocking=true&result=true"\
 -X POST -H  "Content-Type: application/json" -d \
 '{"__post_data":{"loginId": "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f","enableStateQuery": false,"enableTravelDateQuery": false,"enableBoughtDateQuery": false,"travelDateStart": null,"travelDateEnd": null,"boughtDateStart": null,"boughtDateEnd": null}}'
"""

session = requests.Session()
session.auth = constant.WHISK_AUTH_TUPLE
auth = constant.WHISK_AUTH_TUPLE

class ServerlessTrainTicket:
    def __init__(self):
        self.orders = []
        self.contacts = []
    
    def pick_random_travel(self):
        # Always up-to-date
        self.travels = self.get_left_trip_tickets()
        """
        NOTE: Some travel information may be empty and
        random.choice() cannot be applied.
        """
        return random.choice(self.travels) if self.travels else []

    def pick_order(self):
        if not len(self.orders):
            self.query_orders_for_refresh()
        return random.choice(self.orders)
    
    def pick_random_contact(self):
        self.contacts = self.find_contacts_by_accoundId()
        return random.choice(self.contacts)

    def get_random_depature_time(self):
        now = datetime.now() + timedelta(days=random.randint(0, 10))
        return now.strftime("%Y-%m-%d")
        
    def query_orders_for_refresh(self):
        action_name = '/guest/query-orders-for-refresh'
        params = api_config[action_name]['params']
        api = action_api[action_name]
        url = f"{constant.WHISK_APIHOST_HTTPS}{api}"
        
        response = session.post(url, json=params, verify=False)
        self.orders=response.json()['data']
        # save orders for 'pay' or 'cancel'
        return self.orders

    def get_left_trip_tickets(self):
        def place_pair():
            station_list = ["Shang Hai", "Shang Hai Hong Qiao", "Tai Yuan", "Bei Jing", "Nan Jing", "Shi Jia Zhuang", "Xu Zhou", "Ji Nan", "Hang Zhou", "Jia Xing Nan", "Zhen Jiang", "Wu Xi", "Su Zhou"]
            # return random.sample(station_list, 2)
            return ["Shang Hai", "Su Zhou"] # for test

        action_name = '/guest/get-left-trip-tickets'
        params = api_config[action_name]['params']
        departure_time = self.get_random_depature_time()
        # Update datetime
        params["__post_data"] = {
            "startingPlace": place_pair()[0],
            "endPlace": place_pair()[1],
            "departure_time": departure_time,
        }
        print(place_pair(), departure_time)

        api = action_api[action_name]
        url = f"{constant.WHISK_APIHOST_HTTPS}{api}"
        response = session.post(url, json=params, verify=False)
        return response.json()['data']

    def preserve_ticket(self):
        def pick_random_seat_type():
            seat_types = ["2", "3"]
            return random.choice(seat_types)
            
        travel = self.pick_random_travel()
        if not travel:
            print("Not travel, return...")
            return
        action_name = "/guest/preserve-ticket"
        params = api_config[action_name]['params']
        departure_time = self.get_random_depature_time()
        contact = self.pick_random_contact()
        trip_id = f"{travel['tripId']['type']}{travel['tripId']['number']}"
        # print(f"contact: {contact}")
        params["__post_data"].update({
            "date": departure_time,
            "accountId": "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f", # -> using default value
            "contactsId": contact['id'],
            "tripId": trip_id,
            "seatType": pick_random_seat_type(), # 2 for 1st class seat,  3 for 2rd class seat, pick randomly
            "from": travel['startingStation'],
            "to": travel['terminalStation'],
            "foodType": 0 # Unknow how to get this param, using default value
        })
        api = action_api[action_name]
        url = f"{constant.WHISK_APIHOST_HTTPS}{api}"
        
        response = session.post(url, json=params, verify=False)
        return response.json()['data']
    
    def pay_for_the_order(self, order):
        order = self.pick_order()
        print(order['id'],order['trainNumber'], order['accountId'],"\n")

        action_name="/guest/pay-for-the-order"
        params = api_config[action_name]['params']
        params["__post_data"]['orderId'] = order['id']
        params["__post_data"]['tripId'] = order['trainNumber']
        params["__post_data"]['userId'] = order['accountId']

        api = action_api[action_name]
        url = f"{constant.WHISK_APIHOST_HTTPS}{api}"
        # print(params)
        response = session.post(url, json=params, verify=False)
        return response.json()

    def cancel_ticket(self, order):
        order = self.pick_order()

        action_name="/guest/cancel-ticket"
        params = api_config[action_name]['params']
        params["orderId"] = order['id']
        params['loginId'] = order['accountId']

        api = action_api[action_name]
        url = f"{constant.WHISK_APIHOST_HTTPS}{api}"
        url = url.replace("{orderId}", params['orderId']).replace("{loginId}", params['loginId'])
        print(f"canceling order: {params['orderId']}")
        
        response = session.get(url, verify=False)
        return response.json()
        
    def find_contacts_by_accoundId(self):
        action_name = '/guest/find-contacts-by-accountid'
        params = api_config[action_name]['params']

        api = action_api[action_name]
        url = f"{constant.WHISK_APIHOST_HTTPS}{api}"
        url = url.replace("{accountId}", params['accountId'])
        print(f"finding contacts of accound: {params['accountId']}...")
        
        response = session.get(url, verify=False)
        return response.json()['data']

tt=ServerlessTrainTicket()
order=tt.pick_order()
# print(tt.cancel_ticket(order=order))
print(tt.pick_random_travel())
# print(tt.find_contacts_by_accoundId())
# print(tt.pick_random_contact())
# print(tt.preserve_ticket())