import os

WHISK_USERNAME_DEFAULT="23bc46b1-71f6-4ed5-8c54-816aa4f8c502"
WHISK_USERNAME=os.environ.get("WHISK_USERNAME", WHISK_USERNAME_DEFAULT)

WHISK_PASSWD_DEFAULT="123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP"
WHISK_PASSWD=os.environ.get("WHISK_PASSWD", WHISK_PASSWD_DEFAULT)

WHISK_AUTH=f"{WHISK_USERNAME}:{WHISK_PASSWD}"


OW_API_HOST_DEFAULT="http://owdev-nginx.openwhisk.svc.cluster.local"
def reslove_ow_api_host():
    print("resloving ow api host")
    return OW_API_HOST_DEFAULT

OW_API_HOST=os.environ.get("__OW_API_HOST", reslove_ow_api_host())

# OpenWhisk apigateway using this suffix for clearing the cached result
ACTION_FLUSH_SUFFIX="__OWK_FLUSH"

# FTP
STORAGE_PATH = f"{os.getcwd()}/file_storage"
FTP_SERVER_HOST = "127.0.0.1"
FTP_SERVER_PORT = 2016