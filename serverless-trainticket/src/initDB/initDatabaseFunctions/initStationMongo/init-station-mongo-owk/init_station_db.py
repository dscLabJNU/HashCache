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

    df_to_US = pd.read_csv("../../../others_to_US.csv")
    df_from_US = pd.read_csv("../../../US_to_others.csv")
    stations = set(list(df_to_US['from'].unique()) +
                   list(df_to_US['to'].unique()) +
                   list(df_from_US['to'].unique()) +
                   list(df_from_US['from'].unique())
                   )
    # 转换为列表并排序
    stations = sorted(stations)

    inputs = []
    for station in stations:
        inputs.append({
            "id": station.replace(' ', ''),
            "name": station,
            "stayTime": 20
        })
    action_name = "/guest/init-station-mongo"
    params_file = "parameters.json"
    with open(params_file, 'w') as fp:
        json.dump({"stations": inputs}, fp)
    print(f"We have {len(stations)} of stations in total")
    print(invoke_action(name=action_name, params_file=params_file))
