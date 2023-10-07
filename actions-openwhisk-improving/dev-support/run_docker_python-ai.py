import subprocess as sp
import json
import os
import docker
client = docker.from_env()

ts_services=[
    # "ts-serverless-security-mongo", "ts-serverless-config-mongo", "ts-serverless-user-mongo",
    # "ts-serverless-travel-mongo", "ts-serverless-route-mongo", "ts-serverless-train-mongo", 
    # "ts-serverless-price-mongo", "ts-serverless-payment-mongo", "ts-serverless-contacts-mongo",
    # "ts-serverless-order-mongo", "ts-serverless-station-mongo", "ts-serverless-inside-payment-mongo",
    # "ts-serverless-auth-mongo", 
    # "ts-auth-service", "ts-verification-code-service", "ts-serverless-ui-dashboard",
    # HashCache Global Proxy
    "hashcache-global-proxy"
    ]
owk_services=[
    "owdev-apigateway"
]

def dump_host_name(json_name, services, namespace="default"):

    ts_services_actual=[]
    # Get actual instance name
    for service in services:
        cmd=f"kubectl get pod -o wide -n {namespace} | grep {service} | awk '{{print $1}}'"
        instance_name=sp.check_output(cmd, shell=True).decode("utf-8").strip()
        ts_services_actual.append(instance_name)

    service_ip_mapper={}
    for instance_name in ts_services_actual:
        cmd=f"kubectl get pod -n {namespace} {instance_name}" + " --template '{{.status.podIP}}'"
        # print(cmd)
        ip=sp.check_output(cmd, shell=True).decode('utf-8').rstrip()
        # print(f"{service} -> {ip}")
        service_ip_mapper[instance_name]=ip    

    with open(json_name, "w") as f:
        json.dump(service_ip_mapper, f)

def get_service_mapper(json_name, services, namespace="default"):
    if not os.path.exists(json_name):
        dump_host_name(json_name=json_name, services=services, namespace=namespace)

    with open(json_name, 'r') as load_f:
        instance_ip_json=json.load(load_f)

    format_str="--add-host={}:{} "
    add_host_str=""
    for instance_name, ip in instance_ip_json.items():
        if ip == "<no value>":
            print(f"ATTENTION!!! {instance_name} not {ip}")
            continue
        arrays = instance_name.split("-")[:-2]
        service_name = "-".join(arrays)
        add_host_str+=format_str.format(f"{service_name}.{namespace}", ip)
    return add_host_str

def run_docker(image_name, api_host_str):
    cmd=f'docker run -i -t -p 8080:8080 {api_host_str} {image_name}'
    sp.call(cmd, shell=True)

if __name__ == '__main__':
    ts_host_name_json="ts_host_name.json"
    owk_gateway_json="owk_gateway.json"
    ts_service_mapper=get_service_mapper(json_name=ts_host_name_json, services=ts_services, namespace='default')
    owk_service_mapper=get_service_mapper(json_name=owk_gateway_json, services=owk_services, namespace='openwhisk')
    
    api_host_str = " ".join([ts_service_mapper, owk_service_mapper])
    print(api_host_str)
    # run_docker(image_name="diomwu/action-python-io-v3.6-ai:HashCache", api_host_str=api_host_str)
    run_docker(image_name="openwhisk/action-python-v3.6-ai:nightly", api_host_str=api_host_str)
    
    