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

    df_from_US = pd.read_csv("../../../US_to_others.csv")

    end_stations = list(df_from_US['to'].unique())
    namespace = uuid.NAMESPACE_URL
    start_name = "United States"
    start_id = start_name.replace(" ", "")
    inputs = []
    for end_station in end_stations:
        uid = str(uuid.uuid5(namespace, end_station))
        end_id = end_station.replace(" ", "")
        inputs.append({
            "id": uid,
            "startStation": start_id,
            "endStation": end_id,
            "stationList": f"{start_id},{end_id}",
            "distanceList": f"0,60000"
        })

    # print(inputs)

    action_name = "/guest/init-route-mongo-owk"
    params_file = "../../route_infos.json"
    with open(params_file, 'w') as fp:
        json.dump({"routes": inputs}, fp)
    print(f"We have {len(end_stations)} of routes in total")
    print(invoke_action(name=action_name, params_file=params_file))
