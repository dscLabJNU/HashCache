import os

############ Used to index config files ############
HOME_DIR="/home/vagrant/HashCache"
UTILS_DIR=f"{HOME_DIR}/serverless-trainticket/src/load-gen/utils"

############ Used to genreate Azure load ############
AZURE_TRACE_ADDR = "/vagrant/share/Azure/AzureFunctionsInvocationTraceForTwoWeeksJan2021/"
AZURE_BENCH_ADDR=f"{HOME_DIR}/serverless-trainticket/src/load-gen/azure_load"
AZURE_NUM_OF_INVOS=5600
AZURE_RPS_PLOT_DIR=f"{HOME_DIR}/serverless-trainticket/src/load-gen/azure_load/imgs"
AZURE_SAMPLE_UNIT="60S"

############ Used to get action API ############
WHISK_USERNAME_DEFAULT="23bc46b1-71f6-4ed5-8c54-816aa4f8c502"
WHISK_USERNAME=os.environ.get("WHISK_USERNAME", WHISK_USERNAME_DEFAULT)

WHISK_PASSWD_DEFAULT="123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP"
WHISK_PASSWD=os.environ.get("WHISK_PASSWD", WHISK_PASSWD_DEFAULT)

WHISK_AUTH=f"{WHISK_USERNAME}:{WHISK_PASSWD}"
WHISK_AUTH_TUPLE=(WHISK_USERNAME,WHISK_PASSWD)

WHISK_APIHOST_DEFAULT="172.10.8.101:31001"
WHISK_APIHOST=os.environ.get("WHISK_APIHOST", WHISK_APIHOST_DEFAULT)
WHISK_APIHOST_HTTPS=f"https://{WHISK_APIHOST}"

WHISK_API_GATEWAY_DEFAULT=""
WHISK_API_GATEWAY=os.environ.get("WHISK_API_GATEWAY", WHISK_API_GATEWAY_DEFAULT)
# OpenWhisk apigateway using this suffix for clearing the cached result
ACTION_FLUSH_SUFFIX="__OWK_FLUSH"

# Different Qps in evaluation
LOW_QPS=5
MEDIUM_QPS=15
HIGH_QPS=30
QPS = os.environ.get("evaluate_qps", LOW_QPS)

# Station list csv file
STATION_PATH=f"{HOME_DIR}/serverless-trainticket/src/initDB"