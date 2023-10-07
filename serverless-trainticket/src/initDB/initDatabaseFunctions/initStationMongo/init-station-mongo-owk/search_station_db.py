
from pymongo import MongoClient


import subprocess as sp
import json
import os
import docker
client = docker.from_env()

ts_services = [
    "ts-serverless-station-mongo"
]


def dump_host_name(json_name, services, namespace="default"):

    ts_services_actual = []
    # Get actual instance name
    for service in services:
        cmd = f"kubectl get pod -o wide -n {namespace} | grep {service} | awk '{{print $1}}'"
        instance_name = sp.check_output(
            cmd, shell=True).decode("utf-8").strip()
        ts_services_actual.append(instance_name)

    service_ip_mapper = {}
    for instance_name in ts_services_actual:
        cmd = f"kubectl get pod -n {namespace} {instance_name}" + \
            " --template '{{.status.podIP}}'"
        # print(cmd)
        ip = sp.check_output(cmd, shell=True).decode('utf-8').rstrip()
        # print(f"{service} -> {ip}")
        service_ip_mapper[instance_name] = ip

    with open(json_name, "w") as f:
        json.dump(service_ip_mapper, f)


def get_service_mapper(json_name, services, namespace="default"):
    if not os.path.exists(json_name):
        dump_host_name(json_name=json_name,
                       services=services, namespace=namespace)

    with open(json_name, 'r') as load_f:
        instance_ip_json = json.load(load_f)

    service_ip_mapper = {}
    for instance_name, ip in instance_ip_json.items():
        if ip == "<no value>":
            print(f"ATTENTION!!! {instance_name} not {ip}")
            continue
        arrays = instance_name.split("-")[:-2]
        service_name = "-".join(arrays)
        service_ip_mapper[service_name] = ip
    return service_ip_mapper


if __name__ == "__main__":
    ts_host_name_json = "ts_host_name.json"
    ts_service_mapper = get_service_mapper(
        json_name=ts_host_name_json, services=ts_services, namespace='default')
    target_service = ts_services[0]

    mongo_client = MongoClient(
        f"mongodb://{ts_service_mapper[target_service]}:27017")
    database = mongo_client["ts"]
    collection = database["station"]

    documents = collection.find()
    document_count = collection.count_documents({})

    print(f"{document_count} of entries have been added to mongodb")
    # 打印每个文档的内容
    for document in documents:
        print(document)
