import const
import os
from interceptor_helper import InterceptorHelper
import mitmproxy
from mitmproxy import http
import utils
import urllib


class RequestHandler:
    @classmethod
    def route_request(cls, flow, strategy):
        reqeust_path = flow.request.path
        client_ip = flow.client_conn.peername[0]
        action_name = flow.request.query.get("actionName")

        if "queryIOType" in reqeust_path:
            return cls.query_for_io_type(client_ip, action_name)

        elif "notifyActionName" in reqeust_path:
            return cls.notify_action_name(client_ip, action_name)

        elif "s3" in flow.request.url and strategy=="HashCache":
            return cls.handle_s3_bucket(flow=flow)

        return None

    @staticmethod
    def query_for_io_type(client_ip, action_name):
        """
        For each query, we identify the peername (the remote ip), 
        and search the latest operation to the corresponding resource (W/R/HaventWrittenYet).
        NOTE: We start record the LAST_OP_CLIENT_SEND after first write operation.
        Therefore, querying before producing the request for mongdb returns 'HaventWrittenYet'
        """
        last_op_client_send = InterceptorHelper.get_last_op_client_send(
            client_ip=client_ip)
        encoded_content = last_op_client_send.encode('utf-8')
        # encoded_content = LAST_OP_CLIENT_SEND[client_ip].encode('utf-8')
        print(f"client_ip: {action_name}[{client_ip}] => {encoded_content}")
        return encoded_content

    @staticmethod
    def notify_action_name(client_ip, action_name):
        """
        Before the action start, it first send a request to let the proxy
        know the relationship between action_name and IP.
        Then the relationship (IP_ACTION) can be used in 'queryIOType' interface
        """
        print(f"Binding IP: {action_name} with: {client_ip}")
        InterceptorHelper.set_IP_action(client_ip, action_name)
        # IP_ACTION[client_ip] = action_name
        return b"Notcie ActionName Succefully!"

    @staticmethod
    def handle_s3_bucket(flow):
        flow.request.headers["file_exsited"] = 'False'
        request_url = urllib.parse.unquote(flow.request.url)
        saved_file_name = str(hash(request_url))
        flow.request.headers['hash_url'] = saved_file_name
        if utils.check_file_exsited_storage(saved_file_name) and flow.request.method == "GET":
            # ftp服务是http的
            flow.request.scheme = 'http'
            flow.request.host = const.FTP_SERVER_HOST
            flow.request.headers['Host'] = const.FTP_SERVER_HOST
            flow.request.port = const.FTP_SERVER_PORT
            flow.request.path = os.path.join(
                const.STORAGE_PATH, saved_file_name)
            flow.request.headers['file_exsited'] = "True"

            print(
                f"redirecting reqeusts to:{const.FTP_SERVER_HOST}:{const.FTP_SERVER_PORT}")
            
            # Only redirect the request
            return None
        # Fetch the S3 object via Internet
        return None