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

function clear_api(){
  # 执行 wsk -i api list 命令，并将输出结果存储到变量 api_list 中
  api_list=$(wsk -i api list)

  # 在输出结果中查找是否有 API Name 为 /hotelReservation 的 API
  if echo "$api_list" | grep -q "/hotelReservation"; then
    echo "API /hotelReservation found, deleting..."
    
    # 执行 wsk -i api delete /hotelReservation 命令来删除 API
    wsk -i api delete /hotelReservation
    
    # 检查 API 是否被成功删除
    if [ $? -eq 0 ]; then
      echo "API /hotelReservation deleted successfully"
    else
      echo "Failed to delete API /hotelReservation"
    fi
  else
    echo "API /hotelReservation not found"
  fi
}

buildFunction(){
    action=$1
    runtime=$2
    
    cd $action
    rm -rf *.zip
    echo "BUILDING $action with runtime: $runtime..."
    bash build-action.sh $runtime 2>&1 > /dev/null
    cd ..
    echo "FINISHED $action"
}

function do_build(){
    for action in */
    do
        buildFunction $action $runtime
    done
    
    # 检查 API 数量是否为 8
    local count=$(wsk -i api list | grep /guest/ | wc -l)
    if [ $count -ne 8 ]; then
      echo "API count is $count, retrying..."
      # 如果 API 数量不为 8，继续执行 do_build 函数
      return 1
    fi

    echo "Build owk functions successfully"
    return 0
}

function main(){
  local strategy=$1
  # 执行 do_build 函数
  retry_count=0
  while true; do
    clear_api
    if do_build "$strategy"; then
      break
    fi

    retry_count=$(( retry_count + 1 ))
    if [ $retry_count -ge 3 ]; then
      echo "Failed to build after 3 retries"
      exit 1
    fi
    sleep 1
  done
}

wait_owk_server
wait_owk_api_gateway
clear_api

strategy="$1"
case "$strategy" in
  HashCache)
    runtime="python-io:3"
    main $strategy
    ;;
  FaaSCache)
    runtime="python:3"
    main $strategy
    ;;
  OpenWhisk)
    runtime="python:3"
    main $strategy
    ;;
  *)
    echo "Invalid strategy: $strategy"
    echo "Usage: $0 [HashCache, FaaSCache, OpenWhisk]"
    exit 1
    ;;
esac
