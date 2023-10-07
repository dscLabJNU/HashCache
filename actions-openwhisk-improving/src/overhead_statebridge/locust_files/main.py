from locust import task, FastHttpUser, between, TaskSet, events
import logging
import json
import itertools
import random


file_sizes = ["1", "16", "32", "126", "256",
              "512", "1024", "2048", "3072", "4096"]  # in KB
inputs = itertools.cycle({"origin_img": file_size} for file_size in file_sizes)


class MyTaskSet(TaskSet):

    def general_post_action(self, action_name, api, params):
        with self.client.post(api, json=params, catch_response=True) as resp:
            if resp.status_code != 200:
                logging.error(
                    f"invoke action: {action_name} got status code={resp.status_code}")
        # logging.debug(f"invoking action {action_name}...")
        # self.client.post(api, json=params)

    # 定义要测试的 Action 名称列表
    action_names = [f"blob_cache_{i}" for i in range(1, 5+1)]

    @task
    def test_action1(self):
        action_name = self.action_names[random.randint(
            0, len(self.action_names) - 1)]
        api = f"https://172.10.8.101:31001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/overhead/{action_name}"
        self.general_post_action(
            action_name=action_name, params=next(inputs), api=api)

    @task
    def test_action2(self):
        action_name = self.action_names[random.randint(
            0, len(self.action_names) - 1)]
        api = f"https://172.10.8.101:31001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/overhead/{action_name}"
        self.general_post_action(
            action_name=action_name, params=next(inputs), api=api)

    @task
    def test_action3(self):
        action_name = self.action_names[random.randint(
            0, len(self.action_names) - 1)]
        api = f"https://172.10.8.101:31001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/overhead/{action_name}"
        self.general_post_action(
            action_name=action_name, params=next(inputs), api=api)

    @task
    def test_action4(self):
        action_name = self.action_names[random.randint(
            0, len(self.action_names) - 1)]
        api = f"https://172.10.8.101:31001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/overhead/{action_name}"
        self.general_post_action(
            action_name=action_name, params=next(inputs), api=api)

    @task
    def test_action5(self):
        action_name = self.action_names[random.randint(
            0, len(self.action_names) - 1)]
        api = f"https://172.10.8.101:31001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/overhead/{action_name}"
        self.general_post_action(
            action_name=action_name, params=next(inputs), api=api)

    @task
    def test_action6(self):
        action_name = self.action_names[random.randint(
            0, len(self.action_names) - 1)]
        api = f"https://172.10.8.101:31001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/overhead/{action_name}"
        self.general_post_action(
            action_name=action_name, params=next(inputs), api=api)

    @task
    def test_action7(self):
        action_name = self.action_names[random.randint(
            0, len(self.action_names) - 1)]
        api = f"https://172.10.8.101:31001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/overhead/{action_name}"
        self.general_post_action(
            action_name=action_name, params=next(inputs), api=api)

    @task
    def test_action8(self):
        action_name = self.action_names[random.randint(
            0, len(self.action_names) - 1)]
        api = f"https://172.10.8.101:31001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/overhead/{action_name}"
        self.general_post_action(
            action_name=action_name, params=next(inputs), api=api)

    @task
    def test_action9(self):
        action_name = self.action_names[random.randint(
            0, len(self.action_names) - 1)]
        api = f"https://172.10.8.101:31001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/overhead/{action_name}"
        self.general_post_action(
            action_name=action_name, params=next(inputs), api=api)

    @task
    def test_action10(self):
        action_name = self.action_names[random.randint(
            0, len(self.action_names) - 1)]
        api = f"https://172.10.8.101:31001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/overhead/{action_name}"
        self.general_post_action(
            action_name=action_name, params=next(inputs), api=api)


class MyUser(FastHttpUser):
    tasks = [MyTaskSet]
