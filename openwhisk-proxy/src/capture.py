from typing import List, Text
import mitmproxy
from mitmproxy import ctx
from mitmproxy import http
import urllib, os, subprocess

STORAGE_PATH = f"{os.getcwd()}/file_storage"
WEB_DIS_SERVER = "http://127.0.0.1:7379"
FTP_SERVER_HOST = "127.0.0.1"
FTP_SERVER_PORT = 2016

def save_files(saved_file_name: str, response_content: bytes):
    # 将二进制流保存到redis中
    # self.redis_conn.set(saved_file_name, response_content)

    # 将二进制流保存到本地文件
    saved_file_path = os.path.join(STORAGE_PATH, saved_file_name)
    with open(saved_file_path, 'wb') as f:
        f.write(response_content)
    print(f"file has saved in {saved_file_path}")

    # 将文件保存至webdis中
    # webdis_put_cmd = f"curl -v --upload-file {saved_file_path} {WEB_DIS_SERVER}/SET/{saved_file_name}"
    # print(webdis_put_cmd)
    # subprocess.call(webdis_put_cmd, shell=True)


def check_webdis_exsited(file_name: str):
    print("CHECKING IF THE FILE EXISTED IN WEBDIS")
    webdis_get_cmd = f"curl -vs {WEB_DIS_SERVER}/GET/{file_name} -o out"
    print(webdis_get_cmd)
    # subprocess.call(webdis_get_cmd, shell=True)
    return True

def check_file_exsited_storage(file_name: str):
    print(file_name)
    if str(file_name) in os.listdir(STORAGE_PATH):
        print("file existed")
        return True
    return False

class LifecycleEvents:
    """"""

    def load(self, loader: mitmproxy.addonmanager.Loader):
        """
        Called when an addon is first loaded. This event receives a Loader
        object, which contains methods for adding options and commands. This
        method is where the addon configures itself.
        """
        subprocess.call(f'mkdir -p {STORAGE_PATH}', shell=True)
        # self.redis_pool = utils.RedisPool(host="127.0.0.1", port=6379, db=0)
        # self.redis_conn = self.redis_pool.redis_connect()

    def requestheaders(self, flow: mitmproxy.http.HTTPFlow):
        pass

    def request(self, flow: mitmproxy.http.HTTPFlow):
        flow.request.headers["file_exsited"] = 'False'
        request_url = urllib.parse.unquote(flow.request.url)
        saved_file_name = str(hash(request_url))
        flow.request.headers['hash_url'] = saved_file_name
        if check_file_exsited_storage(saved_file_name) and flow.request.method == "GET":
            # ftp服务是http的
            flow.request.scheme = 'http'
            flow.request.host = FTP_SERVER_HOST
            flow.request.headers['Host'] = FTP_SERVER_HOST
            flow.request.port = FTP_SERVER_PORT
            flow.request.path = os.path.join(STORAGE_PATH, saved_file_name)
            flow.request.headers['file_exsited'] = "True"
            
            print(f"redirecting reqeusts to:{FTP_SERVER_HOST}:{FTP_SERVER_PORT}")

    def response(self, flow: mitmproxy.http.HTTPFlow):
        response_content = flow.response.content
        saved_file_name = flow.request.headers['hash_url']
        # print(len(flow.response.content))
        # Todo 异步请求
        if flow.request.headers['file_exsited'] == "False" and flow.request.method == 'GET':
            save_files(saved_file_name, response_content)


addons = [
    LifecycleEvents()
]
