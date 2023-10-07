import re
from shell import shell
import pandas as pd
import os


def write_csv(LOG_FILE, namespcace='openwhisk'):
    # deprecated
    faas_pod_names = shell(
        f'kubectl get pods --no-headers -o custom-columns=":metadata.name" -n {namespcace}'
    ).output()
    faas_pod_names = list(filter(lambda x: 'guest' in x, faas_pod_names))
    log_file = open(LOG_FILE, 'w')
    print("func_name,hash_input,hash_output,duration(ms)",
          file=log_file,
          flush=True)
    for pod_name in faas_pod_names:
        print(pod_name)
        all_logs = shell(f'kubectl logs -n {namespcace} {pod_name}').output()

        enc_regx = re.compile('(?<=FunctionLog:\ ).*$', re.UNICODE)
        function_logs = list(filter(lambda x: "FunctionLog" in x, all_logs))
        for log in function_logs:
            string_line = re.search(enc_regx, log).group()
            print(string_line, file=log_file, flush=True)


def analyze_function_log(LOG_FILE):
    data = pd.read_csv(LOG_FILE)
    num_total_func = data['func_name'].nunique()
    num_all_invokes = data['func_name'].count()
    # duration_all_func = data['duration(ms)'].sum()

    # Distinguishes computational functions from others
    comp_func = data.groupby(
        ["func_name",
         'hash_input']).filter(lambda x: x['hash_output'].nunique() == 1)
    num_comp_invokes = comp_func['func_name'].count()
    num_comp_func = comp_func['func_name'].nunique()

    # Duplicated(keep=False) counts all same values.
    duplicated_func_of_computational = comp_func[comp_func.duplicated(
        ['func_name', 'hash_input'], keep=False)]

    num_duplicated_invokes = duplicated_func_of_computational[
        'func_name'].count()
    # duration_duplicated_invokes = duplicated_func_of_computational[
        # 'duration(ms)'].sum()

    result = {
        "P_num_comp": 100 * num_comp_func / num_total_func,
        "P_invo_comp": 100 * num_comp_invokes / num_all_invokes,
        "P_invo_dup": 100 * num_duplicated_invokes / num_comp_invokes,
        # "P_time_dup": 100 * duration_duplicated_invokes / duration_all_func,
    }
    print(result)


if __name__ == "__main__":
    LOG_FILE = "./function_input_output_log.csv"
    # if not os.path.exists(LOG_FILE):
    #     write_csv(LOG_FILE)
    analyze_function_log(LOG_FILE)