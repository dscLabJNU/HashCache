#!/bin/bash
source const.sh

function run_monitor(){
    local strategy=$1
    local app_name=$2
    local remote_hosts=${@:3}
    bash $path_to_resource_monitor/remote_monitor.sh $strategy $app_name $remote_hosts
}

function clear_monitor(){
    local remote_hosts=${@:1}
    source $path_to_resource_monitor/clear_monitor.sh
    stop_monitor $remote_hosts
}

function usage() {
    echo -e "Usage: $0 [HashCache] [num_inputs (int)]"
}

function lauch_owk(){
    strategy=$1
    cd $path_to_openwhisk_deploy_kube
    bash swiching_openwhisk_version.sh $strategy
    bash delete-invoke-pods.sh
    # bash delete-invokers.sh
    bash delete-controllers.sh
    cd -
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

function build_owk_function(){
    wait_owk_server
    wait_owk_api_gateway
    wsk api delete -i /overhead
    
    cd ./src/overhead_actionmapper
    bash build-action.sh
    cd -
}

function run_benchmark(){
    strategy=$1
    app_name=$2
    num_input_pairs=$3
    
    remote_hosts="serverless-node-01 serverless-node-02 serverless-node-03 serverless-node-04 serverless-node-05"
    # Run monitor before evaluation
    run_monitor $strategy $app_name $remote_hosts
    
    # Evaluation
    cd ./src/overhead_actionmapper/
    bash run_load.sh $strategy $num_input_pairs
    cd -


    # Clear monitor after evaluation
    clear_monitor $remote_hosts

}

function main() {
    strategy=$1
    app_name=$2
    num_inputs=$3
    lauch_owk $strategy

    build_owk_function $strategy
    run_benchmark $strategy $app_name $num_inputs
}

if [[ $# -lt 2 ]]; then
    usage
    exit
else
    ulimit -n 100000
    strategy=$1
    num_inputs=$2
    case "$strategy" in
    "HashCache" | "FaaSCache" | "OpenWhisk")
        main $strategy "ActionMapperOverhead" $num_inputs
        ;;
    *) # default
        usage
        exit
        ;;
    esac
fi
