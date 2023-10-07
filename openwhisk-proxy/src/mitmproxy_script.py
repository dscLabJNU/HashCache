import mitmproxy
from mitmproxy import ctx, tcp, http
from interceptor_helper import InterceptorHelper
from request_handler import RequestHandler
from response_handler import ResponseHandler
import traceback
import subprocess
import const
import urllib
import time
import os

STRATEGY=os.getenv('STRATEGY')
print(f"Running State bridge with strategy: {STRATEGY}")

class MongoDBInterceptor:

    def load(self, loader: mitmproxy.addonmanager.Loader):
        """
        Called when an addon is first loaded. This event receives a Loader
        object, which contains methods for adding options and commands. This
        method is where the addon configures itself.
        """
        # Resolve the DNS, only for local dev
        InterceptorHelper.resolve_owk_gw()
        
        # Create FTP storage dir
        subprocess.call(f'mkdir -p {const.STORAGE_PATH}', shell=True)
            

    def tcp_message(self, flow):
        if STRATEGY == "HashCache":
            # 检查是否为 MongoDB 查询请求, MongoDB 默认端口号为 27017
            if flow.server_conn.address[1] == 27017: 
                client_ip = flow.client_conn.peername[0]
                client_port = flow.client_conn.peername[1]
                client_op = "Unknown"
                server_ip = flow.server_conn.peername[0]
                try:
                    data = flow.messages[-1].content
                    InterceptorHelper.identify_client_op(client_ip, server_ip, data)
                except Exception as ex:
                    traceback.print_exc()

    def request(self, flow):
        request_host_name = flow.request.host
        if "owdev-apigateway" in request_host_name and not InterceptorHelper.in_k8s_env():
            # Only for local dev, resolve the domian name
            flow.request.host = InterceptorHelper.get_name_server(domain="owdev-apigateway")

        response_content = RequestHandler.route_request(flow, STRATEGY)
        if response_content:
            flow.response = http.Response.make(
                200,
                response_content,
                {"Content-Type": "application/json"},
            )
    
    def response(self, flow):
        if STRATEGY == "HashCache":
            ResponseHandler.route_request(flow=flow)
        request_url = urllib.parse.unquote(flow.request.url)
        duration = time.time() - flow.timestamp_start
        print(f"[FetchingState] It tooks {duration} seconds to process request: {request_url}")
     

addons = [
    MongoDBInterceptor()
]