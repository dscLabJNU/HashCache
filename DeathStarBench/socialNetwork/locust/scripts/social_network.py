from locust import FastHttpUser, constant, task, TaskSet
import time
import random

log_csv = open("locust_function_log.csv", "w")
print("func_name,hash_input,hash_output,duration(ms)", file=log_csv, flush=True)

charset = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's',
           'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'Q',
           'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H',
           'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '1', '2', '3', '4', '5',
           '6', '7', '8', '9', '0']

decset = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


max_user_index = 96
text_len = 25
num_user_mentions = 5
num_urls = 5
num_media = 4
home_start = 0
home_stop = 10
user_start = 0
user_stop = 10


def stringRandom(length):
    if length > 0:
        return stringRandom(length - 1) + random.choice(charset)
    else:
        return ""


def decRandom(length):
    if length > 0:
        return decRandom(length - 1) + random.choice(decset)
    else:
        return ""


class Task(TaskSet):
    def record(self, function_name, hash_input, hash_output, duration):
        print(f"{function_name},{hash_input},{hash_output},{duration}",
              file=log_csv, flush=True)

    @task
    def compose_post(self):
        user_index = random.randint(0, max_user_index - 1)
        username = "username_" + str(user_index)
        user_id = str(user_index)
        text = stringRandom(text_len)
        media_ids = '['
        media_types = '['

        for i in range(num_user_mentions + 1):
            user_mention_id = None
            while True:
                user_mention_id = random.randint(0, max_user_index - 1)
                if user_index != user_mention_id:
                    break
            text = text + " @username_" + str(user_mention_id)

        for i in range(num_urls + 1):
            text = text + " http://" + stringRandom(64)

        for i in range(num_media + 1):
            media_id = decRandom(18)
            media_ids = media_ids + "\"" + media_id + "\","
            media_types = media_types + "\"png\","

        media_ids = media_ids[:-1] + "]"
        media_types = media_types[:-1] + "]"

        method = "POST"
        path = "/wrk2-api/post/compose"
        headers = {}
        body = ""

        headers["Content-Type"] = "application/x-www-form-urlencoded"

        if num_media:
            body = {"username": username,
                    "user_id": user_id,
                    "text": text,
                    "media_ids": media_ids,
                    "media_types": media_types,
                    "post_type": "0"}
        else:
            body = {"username": username,
                    "user_id": user_id,
                    "text": text,
                    "media_ids": "",
                    "post_type": "0"}

        hash_input = hash(path)
        start = time.time()
        response = self.client.post(path, data=body)
        duration = time.time() - start
        hash_output = hash(response.text)
        self.record(function_name="compose_post", hash_input=hash_input,
                    hash_output=hash_output, duration=duration)

    @task
    def read_user_timeline(self):
        user_id = random.randint(0, max_user_index - 1)
        start = user_start
        stop = user_stop
        args = "user_id=" + str(user_id) + "&start=" + \
            str(start) + "&stop=" + str(stop)
        path = "http://localhost:8080/wrk2-api/user-timeline/read?" + args
        hash_input = hash(path)
        start = time.time()
        response = self.client.get(path)
        duration = time.time() - start
        hash_output = hash(response.text)
        self.record(function_name="read_user_timeline", hash_input=hash_input,
                    hash_output=hash_output, duration=duration)

    # @task
    # def read_home_timeline(self):
    #     user_id = str(random.randint(0, max_user_index - 1))

    #     start = home_start
    #     stop = home_stop

    #     args = "user_id=" + str(user_id) + "&start=" + \
    #         str(start) + "&stop=" + str(stop)
    #     method = "GET"
    #     headers = {}
    #     headers["Content-Type"] = "application/x-www-form-urlencoded"
    #     path = "http://localhost:8080/wrk2-api/home-timeline/read?" + args
    #     # return wrk.format(method, path, headers, nil)
    #     hash_input = hash(path)
    #     start = time.time()
    #     response = self.client.get(path)
    #     duration = time.time() - start
    #     hash_output = hash(response.text)
    #     self.record(function_name="read_home_timeline", hash_input=hash_input,
    #                 hash_output=hash_output, duration=duration)


class MyUser(FastHttpUser):
    RPS = 100
    wait_time = constant(1/RPS)
    tasks = [Task]
