import os
from collections import defaultdict
import subprocess as sp
import requests
import const

WRITE_OP="W"
READ_OP="R"
OTHER_OPS="HaventWrittenYet"
# 记录每个 IP 地址发过来的最后一次操作，W/R (write or read)，线程安全
LAST_OP_CLIENT_SEND = defaultdict(lambda:OTHER_OPS)
SERVICE_ACTION = defaultdict(set) # service (mongodb) 服务过的 action
IP_ACTION = {} # IP 地址对应的 action_name

# 在本地开发时需要解析的DNS域名集合
DOMAINs = [
    "owdev-apigateway"
]
# 记录DNS域名对应的IP地址
NAME_SERVER = {}

class InterceptorHelper:
    @staticmethod
    def get_name_server(domain: str):
        # NAME_SERVER['owdev-apigateway']
        print(f"Getting domain's[{domain}] IP")
        return NAME_SERVER.get(domain)
    
    @staticmethod
    def get_last_op_client_send(client_ip):
        return LAST_OP_CLIENT_SEND[client_ip]
    
    @staticmethod
    def set_IP_action(client_ip, action_name):
        IP_ACTION[client_ip] = action_name

    @staticmethod
    def in_k8s_env():
        """
        In k8s env (openwhisk namespace), KUBERNETES_PORT env will automatically import into the container
        So we do not need to resolve the openwhisk-apigateway's domain name
        """
        return os.environ.get("KUBERNETES_PORT", None)

    @classmethod
    def resolve_owk_gw(cls, namespace='openwhisk'):
        if cls.in_k8s_env():
            print("You are in k8s environment")
            return
        print("You are in local environment")
        for domain in DOMAINs:
            cmd = f"kubectl get service {domain} -n {namespace} -o jsonpath='{{.spec.clusterIP}}'"
            ip = sp.check_output(cmd, shell=True).decode("utf-8").strip()
            NAME_SERVER[domain] = ip
        print(f"Resolved domain names: {NAME_SERVER}")

    @classmethod
    def identify_client_op(cls, client_ip, server_ip, data):
        """
        识别客户端的请求, 当mimtproxy接收到 /queryForIOType 请求时
        做出反馈, 以识别 client_ip 容器对应的函数发出的请求类型
        """
        client_operation = OTHER_OPS
        # action_name shoud not be None, since we notify the proxy the action_name before action starts
        action_name = IP_ACTION.get(client_ip, None)
        if b'update' in data or b'insert' in data:
            print(f"SERVICE_ACTION[{server_ip}]: {SERVICE_ACTION[server_ip]}")
            if SERVICE_ACTION[server_ip]:
                
                # This service has already served read requests from other IPs
                cls.flush_action_cache(server_ip)

            # always up-to-date
            LAST_OP_CLIENT_SEND[client_ip] = WRITE_OP
            print(f"Action [{action_name or 'Unknown'}]: {client_ip} -> [{WRITE_OP}] -> {server_ip}")

        elif b'find' in data:
            # always up-to-date
            LAST_OP_CLIENT_SEND[client_ip] = READ_OP
            SERVICE_ACTION[server_ip].add(action_name)
            print(f"Action [{action_name or 'Unknown'}]: {client_ip} -> [{READ_OP}] -> {server_ip}")

        print(f"The last operation sent by client [{client_ip}({action_name})] is [{LAST_OP_CLIENT_SEND[client_ip]}]")
    
    @staticmethod
    def build_flush_request(action: str, namespace: str='guest'):
        # curl -u ${const.WHISK_AUTH} ${__OW_API_HOST}/api/v1/namespaces/guest/actions/${action_name}${const.ACTION_FLUSH_SUFFIX} 
        """
        action: /guest/get-stationid-list-by-name-list
            -> namespace: guest
            -> action_name: get-stationid-list-by-name-list
        """
        _, namespace, action_name = slices = action.split("/")
        print(f"aciton_name: {action_name}, const.ACTION_FLUSH_SUFFIX: {const.ACTION_FLUSH_SUFFIX}")
        print(f"{action_name}{const.ACTION_FLUSH_SUFFIX}")
        request_url = f"{const.OW_API_HOST}/api/v1/namespaces/{namespace}/actions/{action_name}{const.ACTION_FLUSH_SUFFIX}"
        return request_url

    @classmethod
    def flush_action_cache(cls, server_ip):
        for action in SERVICE_ACTION[server_ip]:
            print(f"===== Flushing action cache: [{action}] =====")
            request_url = cls.build_flush_request(action)
            print(f"Request url: {request_url}")
            response = requests.get(request_url, auth=(const.WHISK_USERNAME, const.WHISK_PASSWD))
            print(f"Flushing response: {response}")