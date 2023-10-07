from owk_invoke import OwkFunction
import constant
import urllib3
import requests
from locust import TaskSet, task, tag
from locust.exception import RescheduleTask
from datetime import datetime, timedelta
import random
import time
import logging
import json
import sys
sys.path.append("../")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# args = owk_function.user_login()
# args = owk_function.recommend()
# args = owk_function.search_hotel()
# args = owk_function.reserve()
# print(main(args))import time

with open(f'{constant.UTILS_DIR}/api_config.json') as f:
    api_config = json.load(f)

with open(f'{constant.UTILS_DIR}/action_api.json') as f:
    action_api = json.load(f)


owk_function = OwkFunction()
LOG_FILE = open("locust_api_log.csv", "w")
print(f"func_name,hash_input,hash_output,duration", file=LOG_FILE, flush=True)


class SingleTask(TaskSet):
    def flush_action_cache(self, action):
        _, namespace, action_name = action.split("/")
        request_url = f"{constant.WHISK_APIHOST_HTTPS}/api/v1/namespaces/{namespace}/actions/{action_name}{constant.ACTION_FLUSH_SUFFIX}"
        logging.debug(f"Request url: {request_url}")
        response = requests.get(request_url, auth=(
            constant.WHISK_USERNAME, constant.WHISK_PASSWD), verify=False)
        logging.debug(f"Flushing action: {action}: {response}")

    def general_post_action(self, action_name, params):
        api = action_api[action_name]
        logging.debug(f"invoking action {action_name}... => {params}")
        start = time.time()
        with self.client.post(api, json=params, catch_response=True) as resp:
            if resp.status_code != 200:
                logging.error(
                    f"invoke action: {action_name} got status code={resp.status_code}, now RescheduleTask")
                self.flush_action_cache(action_name)
                raise RescheduleTask()

            resp_json = resp.json()
            if 'data' not in resp_json:
                logging.error(
                    f"invoke action: {action_name} got error({resp_json}), now RescheduleTask")
                self.flush_action_cache(action_name)
                raise RescheduleTask()
            duration = time.time() - start
            print(resp_json)
            print(f"{action_name},{hash(str(params))},{hash(str(resp_json['data']))},{duration}", file=LOG_FILE, flush=True)
            return resp_json['data']

    @task(api_config['/guest/search']['rate'])
    def search_hotel(self):
        action_name="/guest/search"
        args = owk_function.search_hotel()
        self.general_post_action(action_name=action_name, params=args)

    @task(api_config['/guest/user']['rate'])
    def user_login(self):
        action_name="/guest/user"
        args = owk_function.user_login()
        self.general_post_action(action_name=action_name, params=args)
       

    @task(api_config['/guest/recommendation']['rate'])
    def recommend(self):
        action_name="/guest/recommendation"
        args = owk_function.recommend()
        self.general_post_action(action_name=action_name, params=args)
     
    @task(api_config['/guest/reservation']['rate'])
    def reserve(self):
        action_name="/guest/reservation"
        args = owk_function.reserve()
        print(args)
        self.general_post_action(action_name=action_name, params=args)
     