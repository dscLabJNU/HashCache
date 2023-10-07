from locust import FastHttpUser, constant, task, TaskSet
import time
import random

log_csv = open("log.csv", "w")
print("function_name,hash_input,hash_output,duration(ms)", file=log_csv, flush=True)


def get_user():
    id = random.randint(0, 500)
    user_name = f"Cornell_{id}"
    pass_word = ""

    for i in range(10):
        pass_word += str(id)
    return user_name, pass_word


class Task(TaskSet):

    def record(self, function_name, hash_input, hash_output, duration):

        print(f"{function_name},{hash_input},{hash_output},{duration}",
              file=log_csv, flush=True)

    @task(600)
    def search_hotel(self):
        in_date = random.randint(9, 23)
        out_date = random.randint(in_date + 1, 24)

        in_date_str = str(in_date)
        if in_date <= 9:
            in_date_str = f"2015-04-0{in_date_str }"
        else:
            in_date_str = f"2015-04-{in_date_str}"

        out_date_str = str(out_date)
        if out_date <= 9:
            out_date_str = f"2015-04-0{out_date_str}"
        else:
            out_date_str = f"2015-04-{out_date_str}"

        # 定义请求头
        headers = {'Content-Type': 'application/json'}

        lat = 38.0235 + (random.randint(0, 30) - 240.5)/1000.0
        lon = -122.095 + (random.randint(0, 30) - 157.0)/1000.0

        path = "/hotels?inDate=" + in_date_str + "&outDate=" + \
            out_date_str + "&lat=" + str(lat) + "&lon=" + str(lon)
        start = time.time()
        response = self.client.get(path)
        duration = (time.time() - start) / 1000  # converts s to ms
        hash_input = hash(path)
        hash_output = hash(response.text)

        self.record(function_name="search_hotel", hash_input=hash_input,
                    hash_output=hash_output, duration=duration)

    @task(5)
    def user_login(self):
        user_name, password = get_user()
        path = "/user?username=" + user_name + "&password=" + password

        start = time.time()
        response = self.client.post(path)
        duration = (time.time() - start) / 1000  # converts s to ms
        hash_input = hash(path)
        hash_output = hash(response.text)

        self.record(function_name="user_login", hash_input=hash_input,
                    hash_output=hash_output, duration=duration)

    @task(390)
    def recommend(self):
        coin = random.random()
        req_param = ""
        if coin < 0.33:
            req_param = "dis"
        elif coin < 0.66:
            req_param = "rate"
        else:
            req_param = "price"

        lat = 38.0235 + (random.randint(0, 30) - 240.5)/1000.0
        lon = -122.095 + (random.randint(0, 30) - 157.0)/1000.0
        path = "/recommendations?require=" + req_param + \
            "&lat=" + str(lat) + "&lon=" + str(lon)
        start = time.time()
        response = self.client.get(path)
        duration = (time.time() - start) / 1000  # converts s to ms
        hash_input = hash(path)
        hash_output = hash(response.text)

        self.record(function_name="recommend", hash_input=hash_input,
                    hash_output=hash_output, duration=duration)

    @task(5)
    def reserve(self):
        in_date = random.randint(9, 23)
        out_date = in_date + random.randint(1, 5)

        in_date_str = str(in_date)

        in_date_str = str(in_date)
        if in_date <= 9:
            in_date_str = "2015-04-0" + in_date_str
        else:
            in_date_str = "2015-04-" + in_date_str

        out_date_str = str(out_date)
        if out_date <= 9:
            out_date_str = "2015-04-0" + out_date_str
        else:
            out_date_str = "2015-04-" + out_date_str

        hotel_id = str(random.randint(1, 80))
        user_id, password = get_user()
        cust_name = user_id

        num_room = "1"
        lat_str = "nil"
        lon_str = "nil"
        path = "/reservation?inDate=" + in_date_str + "&outDate=" + out_date_str + "&lat=" + lat_str + "&lon=" + lon_str + \
            "&hotelId=" + hotel_id + "&customerName=" + cust_name + "&username=" + \
            user_id + "&password=" + password + "&number=" + num_room
        start = time.time()
        response = self.client.post(path)
        duration = (time.time() - start) / 1000  # converts s to ms
        hash_input = hash(path)
        hash_output = hash(response.text)

        self.record(function_name="reserve", hash_input=hash_input,
                    hash_output=hash_output, duration=duration)


class MyUser(FastHttpUser):
    RPS = 100
    wait_time = constant(1/RPS)
    tasks = [Task]
