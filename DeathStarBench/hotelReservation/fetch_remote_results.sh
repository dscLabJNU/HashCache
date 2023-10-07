function execRemoteCMD() {
    # execRemoteCMD will execute the commands in the remote host through `ssh`
    remote_host=$1
    ps_command=$2
    exec_command=$3
    filter_result=$(ssh $remote_host $ps_command)
    if [ -n "$filter_result" ]; then
        # echo "Executing: ssh $remote_host '$exec_command'"
        ssh $remote_host "$exec_command"
    else
        echo "Nothing to exec of cmd: [$ps_command] in host [$remote_host]"
    fi
}

function fetch_csvs() {
    local csv_prefix=$1
    local strategy=$2
    local remote_host=$3
    local path_to_save_csvs=$4
    local app_name=$5
    
    source const.sh
    log_path=$path_to_resource_monitor
    csv_file_name=$(printf "${csv_prefix}" "${strategy}" "${app_name}")
    transfered_csv=$(printf "${csv_prefix}" "${strategy}" "${app_name}"_"$remote_host")
    target_host="serverless-node-01"

    printf "Fetching [$csv_file_name] from [$remote_host] and transfer it to [$transfered_csv]\n"
    # 1. Go to the log path and check if there is a target csv file
    filter_log_cmd="cd $log_path; ls $csv_file_name"
    # 2. Execute a sepecific command if pass the $filter_log_cmd
    exec_command="$filter_log_cmd; scp -r $csv_file_name $target_host:$path_to_save_csvs"
    # echo $exec_command
    execRemoteCMD "${remote_host}" "${filter_log_cmd}" "${exec_command}"
    printf "Saving $path_to_save_csvs/$strategy/$transfered_csv...\n\n\n"
    mv "$path_to_save_csvs/$csv_file_name" "$path_to_save_csvs/$strategy/$transfered_csv"
}


strategy=$1
app_name=$2
remote_hosts=${@:3}

utilization_csv_prefix="utilization_%s_%s.csv"
results_dir="$(
    cd "$(dirname "$0")"
    pwd
)/locust/owk/hotel-reservation/logs"

path_to_save_csvs=$results_dir
mkdir -p $path_to_save_csvs

for remote_host in ${remote_hosts[@]}; do
    fetch_csvs $utilization_csv_prefix $strategy $remote_host $path_to_save_csvs $app_name
done