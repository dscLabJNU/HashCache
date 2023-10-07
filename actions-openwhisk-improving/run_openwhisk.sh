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
    echo -e "Usage: $0 [HashCache, FaaSCache, OpenWhisk]"
}

function lauch_owk(){
    strategy=$1
    cd $path_to_openwhisk_deploy_kube
    bash swiching_openwhisk_version.sh $strategy
    cd -
}

function build_owk_function(){
    strategy=$1
    scratch_or_update=$2
    # if [ "$strategy" = "HashCache" ]; then
    cd $path_to_global_proxy
    # restart the StateBridge component
    bash restart_global_proxy_pod.sh $strategy
    cd -
    # fi
    cd $path_to_owk_functions
    bash build-actions.sh $strategy
    cd -
}

function run_benchmark(){
    local qps_level="high"
    local remote_hosts="serverless-node-01 serverless-node-02 serverless-node-03 serverless-node-04 serverless-node-05"
    strategy=$1
    app_name=$2
    # Run monitor before evaluation
    run_monitor $strategy $app_name $remote_hosts
    
    # Evaluation
    cd $path_to_load_gen_dir
    bash run_load.sh $strategy $qps_level
    cd -

    # Analyze activation cold starts
    cd $path_to_analyze_cold_starts
    python3 analyze_cold_starts.py --strategy=$strategy
    cd -
    
    # Analyze fetch_state, function-input-output, and hit_rate (Only for HashCache)
    cd $path_to_load_gen_dir
    bash get_fetch_state_duration_from_global_proxy.sh
    mv fetch_state.csv ./logs/$strategy/${strategy}_fetch_state.csv
    if [ "$strategy" == "HashCache" ]; then
        bash get_function_log_from_owk_controllers.sh
        mv function_input_output_log.csv ./logs/$strategy/${strategy}_function_input_output_log.csv
        
        bash get_hit_rate_from_owk_controllers.sh
        mv hit_rate.csv ./logs/$strategy/${strategy}_hit_rate.csv
    fi
    cd -

    # Clear monitor after evaluation
    clear_monitor $remote_hosts
}

function main() {
    strategy=$1
    app_name=$2

    lauch_owk $strategy

    build_owk_function $strategy
    run_benchmark $strategy $app_name
    bash fetch_all_results.sh
}

if [[ $# -lt 1 ]]; then
    usage
    exit
else
    strategy=$1
    case "$strategy" in
    "HashCache" | "FaaSCache" | "OpenWhisk")
        wsk property set --apihost '172.10.8.101:31001' --auth '23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP'
        main $strategy "FaaSWorkflow"
        ;;
    *) # default
        usage
        exit
        ;;
    esac
fi
