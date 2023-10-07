from locust import FastHttpUser, between, events
import locust
import logging
from tasks import SingleTask
import constant
import random
import time


class User(FastHttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # wait_time = between(0, 1)
    RPS = int(constant.QPS)
    print(f"RPS: {RPS}")
    wait_time = locust.constant(1/RPS)
    tasks = [SingleTask]

    def on_start(self):
        logging.debug('locust user start')

    def on_stop(self):
        logging.debug('locust user stop')


# 定义泊松分布参数
lambda_value = 1.0  # 平均每秒钟发生5次事件
interval_value = 0.2  # 每个事件之间的时间间隔为0.2秒钟


@events.request.add_listener
def my_request_handler(request_type, name, response_time, response_length, response,
                       context, exception, start_time, url, **kwargs):
    wait_time = random.expovariate(lambda_value) * interval_value
    print(f"wait for {wait_time} seconds")
    time.sleep(wait_time)


if __name__ == "__main__":
    size = 100
    wait_times = [random.expovariate(
        lambda_value) * interval_value for _ in range(size)]
    print(f"{sum(wait_times)}秒发完{size}个请求， RPS={size/sum(wait_times)}")
