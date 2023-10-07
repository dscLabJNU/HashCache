#!bin/bash
function prune_env(){
    helm uninstall owdev -n openwhisk
}
prune_env
bash run_actionmapper_overhead.sh FaaSCache 2000

prune_env
bash run_actionmapper_overhead.sh HashCache 2000

prune_env
bash run_actionmapper_overhead.sh OpenWhisk 2000

# Fetch resource utilization
remote_hosts="serverless-node-01 serverless-node-02 serverless-node-03 serverless-node-04 serverless-node-05"
app="ActionMapperOverhead"
bash fetch_remote_results.sh HashCache $app $remote_hosts

bash fetch_remote_results.sh FaaSCache $app $remote_hosts

bash fetch_remote_results.sh OpenWhisk $app $remote_hosts