function execRemoteCMD() {
    remote_host=$1
    ps_command=$2
    exec_command=$3
    filter_result=$(ssh $remote_host $ps_command)
    if [ -n "$filter_result" ]; then
        echo "Executing: ssh $remote_host '$exec_command'"
        ssh $remote_host "$exec_command"
    else
        echo "Nothing to exec of cmd: [$ps_command] in host [$remote_host]"
    fi
}

function stop_monitor() {
    remote_hosts=$@
    echo -e "Cleaning monitor processes in remote hosts..."
    ps_command="ps -ef | grep -v grep |grep -E 'monitor_resources'"
    exec_command="$ps_command | awk '{print \$2}'| xargs kill -9"
    for remote_host in ${remote_hosts[@]}; do
        execRemoteCMD "$remote_host" "${ps_command}" "${exec_command}"
    done
}

