#!/bin/bash

trap 'onCtrlC' INT

function onCtrlC() {
    echo 'capture Ctrl + C'
    clean_monitor
    exit
}

function execRemoteCMD() {
    remote_host=$1
    ps_command=$2
    exec_command=$3
    filter_result=$(ssh "$remote_host" "$ps_command")
    if [ -n "$filter_result" ]; then
        echo "Executing: ssh $remote_host '$exec_command'"
        ssh $remote_host "$exec_command"
    else
        echo "Nothing to exec of cmd: [$ps_command] in host [$remote_host]"
    fi
}

function clean_monitor() {
    remote_hosts=$@
    echo -e "Cleaning monitor processes in remote hosts..."
    ps_command="ps -ef | grep -v grep |grep -E 'monitor_resources'"
    exec_command="$ps_command | awk '{print \$2}'| xargs kill -9"
    
    for remote_host in ${remote_hosts[@]}; do
        execRemoteCMD "$remote_host" "${ps_command}" "${exec_command}"
    done
}


function rm_utilization_log() {
    strategy=$1
    app_name=$2
    remote_hosts=${@:3}
    echo -e "\nRemoving utilization log of strategy ${strategy}_${app_name}"
    rm_utilization_log_cmd="rm -rf ~/HashCache/openwhisk-resource-monitor/utilization_${strategy}_${app_name}.csv"
    for remote_host in ${remote_hosts[@]}; do
        ssh $remote_host $rm_utilization_log_cmd
    done

}

function run_monitor() {
    strategy=$1
    app_name=$2
    remote_hosts=${@:3}
    run_monitor_cmd="cd ~/HashCache/openwhisk-resource-monitor; nohup ./monitor_resources.sh > utilization_${strategy}_${app_name}.csv &"
    for remote_host in ${remote_hosts[@]}; do
        ssh $remote_host $run_monitor_cmd
    done
    echo "Run remote monitor processes done..."
}

function usage() {
    echo -e "Usage: $0 [HashCache, FaaSCache, OpenWhisk] [AppName]"
}

if [[ $# -lt 2 ]]; then
    usage
else
    strategy=$1
    app_name="${2:-default_app}"
    remote_hosts=${@:3}
    echo "Running monitor in [$remote_hosts]"

    clean_monitor $remote_hosts

    rm_utilization_log $strategy $app_name $remote_hosts

    run_monitor $strategy $app_name $remote_hosts
fi
