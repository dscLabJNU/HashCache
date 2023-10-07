import constant
from locust import TaskSet, task, tag, SequentialTaskSet
from locust.exception import RescheduleTask
import numpy as np
import random
import requests
import logging
import json
import sys
import time
sys.path.append("../")


with open(f'{constant.UTILS_DIR}/api_config.json') as f:
    api_config = json.load(f)

with open(f'{constant.UTILS_DIR}/action_api.json') as f:
    action_api = json.load(f)

LOG_FILE = open("locust_api_log.csv", "w")
print(f"func_name,hash_input,hash_output,duration", file=LOG_FILE, flush=True)

class MultiStageAction(TaskSet):
    def flush_action_cache(self, action):
        _, namespace, package, action_name = action.split("/")
        request_url = f"{constant.WHISK_APIHOST_HTTPS}/api/v1/namespaces/{namespace}/actions/{package}/{action_name}{constant.ACTION_FLUSH_SUFFIX}"
        # logging.debug(f"Request url: {request_url}")
        response = requests.get(request_url, auth=(
            constant.WHISK_USERNAME, constant.WHISK_PASSWD), verify=False)
        logging.debug(f"Flushing action: {action}: {response}")

    def general_get_action(self, action_name, api, params=None):
        start = time.time()
        with self.client.get(api, json=params, catch_response=True) as resp:
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
            duration = (time.time() - start) * 1000 # s to ms
            print(f"{action_name},{hash(str(params))},{hash(str(resp_json['data']))},{duration}", file=LOG_FILE, flush=True)
            logging.debug(f"res: {resp.json()}")
            return resp_json['data']
        # start = time.time()
        # logging.debug(f"invoking action {action_name}...")
        # resp = self.client.get(api, json=params)
        # duration = (time.time() - start) * 1000 # s to ms
        # print(f"{action_name},{hash(str(params))},{hash(str(resp.json()))},{duration}", file=LOG_FILE, flush=True)
        # logging.debug(f"res: {resp.json()}")

    #################### APIs Start ####################

    # @task(api_config["/guest/load-gen/map_reduce"]['rate'])
    # def map_reduce(self):

    #     action_name = "/guest/load-gen/map_reduce"
    #     api = action_api[action_name]
    #     self.general_get_action(api=api, action_name=action_name)

    @task(api_config["/guest/load-gen/predict-pipeline"]['rate'])
    def predict_pipeline(self):

        action_name = "/guest/load-gen/predict-pipeline"
        api = action_api[action_name]
        random_image = random.randint(0, 96)
        self.general_get_action(api=api, action_name=action_name, params={"origin_img": random_image})

    @task(api_config["/guest/load-gen/set-computation"]['rate'])
    def set_computation(self):

        action_name = "/guest/load-gen/set-computation"
        api = action_api[action_name]
        self.general_get_action(api=api, action_name=action_name)


class MLWorkflow(SequentialTaskSet):
    def flush_action_cache(self, action):
        _, namespace, action_name = action.split("/")
        request_url = f"{constant.WHISK_APIHOST_HTTPS}/api/v1/namespaces/{namespace}/actions/{action_name}{constant.ACTION_FLUSH_SUFFIX}"
        # logging.debug(f"Request url: {request_url}")
        response = requests.get(request_url, auth=(
            constant.WHISK_USERNAME, constant.WHISK_PASSWD), verify=False)
        logging.debug(f"Flushing action: {action}: {response}")

    def general_post_action(self, action_name, params):
        api = action_api[action_name]
        logging.debug(f"invoking action {action_name}...")
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
            duration = (time.time() - start) * 1000 # s to ms
            print(f"{action_name},{hash(str(params))},{hash(str(resp_json['data']))},{duration}", file=LOG_FILE, flush=True)
            return resp_json['data']

    @task()
    def linear_regression(self):
        action_name = "/guest/linear_regression"
        params = {
            "X": np.random.rand(5, 5).tolist(),
            "y": np.random.rand(5, 1).tolist()
        }
        self.general_post_action(action_name=action_name, params=params)

    @task()
    def rule_match(self):
        action_name = "/guest/rule_match"
        keywords = ['apple', 'banana', 'cherry', 'date', 'elderberry']
        texts = ['This is a text about apple', 'The banana is ripe', 'Cherry pie is my favorite',
                 'Dates are high in sugar']
        params = {
            "keyword": np.random.choice(keywords),
            "text": np.random.choice(texts) + " ".join(np.random.choice(keywords, 1))
        }
        self.general_post_action(action_name=action_name, params=params)

    @task()
    def feature_transform(self):
        action_name = "/guest/feature_transform"
        X = np.random.rand(5, 2)
        y = np.sin(X[:, 0] + X[:, 1])
        params = {
            "X": X.tolist(),
            "y": y.tolist()
        }
        self.general_post_action(action_name=action_name, params=params)

    @task()
    def MLWorkflow(self):
        action_name = "/guest/decision_tree"
        params = {
            "X": np.random.rand(5, 10).tolist(),
            "y": np.random.rand(5, 1).tolist()
        }
        self.general_post_action(action_name=action_name, params=params)
    ################### APIs End ####################
