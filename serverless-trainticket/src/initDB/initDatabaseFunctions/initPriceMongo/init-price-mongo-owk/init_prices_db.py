import pandas as pd
import subprocess
from time import time
import json
import random
import uuid


def invoke_action(name: str, params_file: str, return_code: bool = False):
    popen_args = f"wsk action invoke -i --result {name} "
    popen_args += f"--param-file {params_file}"
    print(popen_args)

    start = time()
    wsk = subprocess.run(args=popen_args, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)
    latency = time() - start
    if wsk.returncode != 0:
        if return_code:
            return {"output": wsk.stderr, "latency": latency, "code": wsk.returncode}
        return {"output": wsk.stderr, "latency": latency}
    if return_code:
        return {"output": json.loads(wsk.stdout.decode()), "latency": latency, "code": 0}
    return {"output": json.loads(wsk.stdout.decode()), "latency": latency}


if __name__ == "__main__":
    with open("../../route_infos.json") as f:
        routes = json.load(f)

    random.seed(42)
    

    inputs = []
    namespace = uuid.NAMESPACE_URL
    for route in routes['routes']:
        uid = str(uuid.uuid5(namespace, route['id']))
        basic_price_rate = round(random.uniform(0.2, 1), 2)
        inputs.append({
            "routeId": route['id'],
            "id": uid,
            "trainType": "gaoTieOne",
            "basicPriceRate": basic_price_rate,
            "firstClassPriceRate": 1.0
        })

    # for inp in inputs:
    #     print(inp)
    action_name = "/guest/init-price-mongo"
    params_file = "parameters.json"
    with open(params_file, 'w') as fp:
        json.dump({"prices": inputs}, fp)
    print(f"We have {len(inputs)} of prices in total")
    print(invoke_action(name=action_name, params_file=params_file))
