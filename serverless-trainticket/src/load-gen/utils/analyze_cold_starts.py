import re
from shell import shell
import argparse
import os

def write_csv(LOG_FILE, namespcace='openwhisk'):
    pod_names = shell(
        f'kubectl get pods --no-headers --selector=name=owdev-invoker -o custom-columns=":metadata.name" -n {namespcace}'
    ).output()
    log_file = open(LOG_FILE, 'w')
    print("activation_id,container_start", file=log_file, flush=True)
    for pod in pod_names:
        all_logs = shell(f'kubectl logs -n {namespcace} {pod}').output()
        function_logs = list(
            filter(lambda x: "containerStart containerState:" in x, all_logs))
        pattern = re.compile(
            r'containerState: (.*) container.* activationId: (.*) ', re.UNICODE)
        for log in function_logs:
            string_line = re.search(pattern, log)
            container_start = string_line.group(1)  # cold or warmed
            activationId = string_line.group(2)
            print(f"{activationId},{container_start}",
                  file=log_file, flush=True)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--strategy", type=str, required=True, choices=[
                        "HashCache", "FaaSCache", "OpenWhisk"], help="Select the running strategy")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    cold_start_log = f"../logs/{args.strategy}"
    os.system(f"mkdir -p {cold_start_log}")
    LOG_FILE = f"{cold_start_log}/{args.strategy}_coldstarts.csv"
    print(LOG_FILE)
    write_csv(LOG_FILE)
