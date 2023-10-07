from azure_load.azure import Azure
# from azure import Azure
import yaml
from collections import namedtuple
import constant


def generate_targets_with_times_azure():
    workflow_infos = yaml.load(open(
        f"{constant.AZURE_BENCH_ADDR}/workflow_infos.yaml"), Loader=yaml.FullLoader)
    workflow_info = workflow_infos[0]

    azure = Azure(workflow_info)
    func_map_dict, app_map_dict = azure.load_mappers()
    num_invos = constant.AZURE_NUM_OF_INVOS
    filter_df = azure.filter_df(app_map_dict, num_invos)
    azure.plot_RPS(filter_df.copy())

    values = filter_df.resample(constant.AZURE_SAMPLE_UNIT, on='invo_ts').count()['func']

    Step = namedtuple("Step", ["users", "dwell"])
    targets_with_times = []
    for index, value in zip(values.index, values):
        dwell = index.total_seconds()
        users = value
        targets_with_times.append(Step(users=users, dwell=dwell))
    print(f"Load Azure trace done: all {len(tuple(targets_with_times))} steps")
    return tuple(targets_with_times)

if __name__=="__main__":
    tartgets = generate_targets_with_times_azure()
    for step, t in enumerate(tartgets):
        print(f"Lauching {t.users} of users in step: {step}")