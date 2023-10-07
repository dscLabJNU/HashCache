#!/bin/bash
set -e

function check_api_server_work(){
    wsk api list -i >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "openwhisk api-gateway work"
    return 0
  else
    echo "openwhisk api-gateway doesn't work"
    return 1
  fi
}

function clear_api(){
    wsk api list -i | awk 'NR>2 {print $3}' | sort | uniq | while read api; do wsk api -i delete "$api"; echo "Deleted API: $api"; done
}

function wait_owk_server(){
    GREEN_SHAN='\E[5;32;49;1m' # 亮绿色闪动
    RES='\E[0m'                # 清除颜色
    i=1
    while true; do
        status_list=$(kubectl get pods -n openwhisk | grep owdev-install | awk '{print $3}')
        for status in $status_list; do
        if [ "$status" == "Completed" ]; then
            echo "At least one instance of owdev is ready"
            return
        fi
        done
        printf "\r${GREEN_SHAN}Waiting for at least one instance of owdev to be ready: %3ds ${RES}" $i
        let i++
        sleep 1
    done
}

function wait_owk_api_gateway(){
    GREEN_SHAN='\E[5;32;49;1m' # 亮绿色闪动
    RES='\E[0m'                # 清除颜色
    i=1
    while true; do
    if check_api_server_work; then
        echo "owdev-gateway is ready"
        return
    else
        printf "\r${GREEN_SHAN}Waiting for owdev-gateway to be ready: %3ds ${RES}" $i
        let i++
        sleep 1
    fi
    done
}

function usage() {
    echo -e "Usage: $0 [HashCache, FaaSCache, OpenWhisk], [update, scratch]"
}

function do_build(){
    local runtime=$1
    ./part02_FaaSFunctions_owk.sh $runtime
    # 检查 API 数量是否为 33
    local count=$(wsk -i api list | grep /guest/ | wc -l)
    if [ $count -ne 33 ]; then
      echo "API count is $count, retrying..."
      # 如果 API 数量不为 33，继续执行 do_build 函数
      return 1
    fi
    echo "Build owk functions successfully"
    return 0
}

declare -A strategyRuntimeMap
strategyRuntimeMap["HashCache"]="java:8-io"
strategyRuntimeMap["OpenWhisk"]="java:8"
strategyRuntimeMap["FaaSCache"]="java:8"

if [[ $# -lt 2 ]]; then
    usage
    exit
else
    strategy=$1
    scratch_or_update=$2
    case "$strategy" in
    "HashCache" | "FaaSCache" | "OpenWhisk")
        runtime=${strategyRuntimeMap[$strategy]}
        echo "Parallel building functions with strategy: [$strategy], runtime: [$runtime]"
        # read -p "Press any key to confirm, or ctrl-C to stop."
        ;;
    *) # default
        usage
        exit
        ;;
    esac
fi
wait_owk_server
wait_owk_api_gateway
./part01_DataBaseDeployment_owk.sh

retry_count=0
while true; do
    clear_api
    if do_build "$runtime"; then
        break
    fi
    retry_count=$(( retry_count + 1 ))
    if [ $retry_count -ge 3 ]; then
        echo "Failed to build after 3 retries"
        exit 1
    fi
    sleep 1
done

if [ $scratch_or_update = "scratch" ]; then
    echo "build from scratch"
    sleep 20
    ./part01_DataInitiation_owk.sh $runtime

    ./part02_BaaSServices.sh

    ./part03_Frontend.sh
    sleep 20
fi