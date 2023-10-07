#!/bin/bash

set -e
function usage() {
    echo -e "Usage: $0 [HashCache, FaaSCache, OpenWhisk]"
}

function call_locust(){
    strategy=$1
    qps_level=$2
    if [ -n "$qps_level" ]; then
        export "evaluate_qps"=${qpsMapper[$qps_level]} # apply in locust_files/main,py
    fi
    locust --config=locust.conf --csv ./logs/$strategy/$strategy
}

declare -A qpsMapper
qpsMapper["low"]=50
qpsMapper["mid"]=100
qpsMapper["high"]=150
if [[ $# -lt 1 ]]; then
    usage
    exit
else
    strategy=$1
    qps_level=$2 # optional
    case "$strategy" in
    "HashCache" | "FaaSCache" | "OpenWhisk")
        mkdir -p ./logs/$strategy
        echo "Run locust benchmark of strategy: [$strategy]"

        # Generate `action_api.json`
        cd utils
        python3 get_action_api.py
        cd -
        
        call_locust $strategy $qps_level
        ;;
    *) # default
        usage
        exit
        ;;
    esac
fi


