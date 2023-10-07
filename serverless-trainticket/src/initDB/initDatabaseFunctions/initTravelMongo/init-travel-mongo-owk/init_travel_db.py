import pandas as pd
import subprocess
from time import time
import json


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
    # print(routes)

    inputs = []
    for index, route in enumerate(routes['routes']):
        inputs.append({
            "tripId": f"D1{index:03d}",
            "trainTypeId": "DongCheOne",
            "routeId": route['id'],
            "startingStationId": route['startStation'],
            "stationsId": route['endStation'],
            "terminalStationId": route['endStation']
        })
    action_name = "/guest/init-travel-mongo"
    params_file = "parameters.json"
    with open(params_file, 'w') as fp:
        json.dump({"travels": inputs}, fp)
    print(f"We have {len(inputs)} of travels in total")
    print(invoke_action(name=action_name, params_file=params_file))
