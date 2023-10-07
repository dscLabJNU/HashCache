#!bin/bash
function prune_env(){
    helm uninstall owdev -n openwhisk
}
# prune_env
# bash run_statebridge_overhead.sh FaaSCache

# prune_env
bash run_statebridge_overhead.sh HashCache

# prune_env
# bash run_statebridge_overhead.sh OpenWhisk

# Fetch resource utilization
remote_hosts="serverless-node-01"
app="StateBridgeOverhead"
bash fetch_remote_results.sh HashCache $app $remote_hosts

# bash fetch_remote_results.sh FaaSCache $app $remote_hosts

# bash fetch_remote_results.sh OpenWhisk $app $remote_hosts