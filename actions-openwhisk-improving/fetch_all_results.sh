remote_hosts="serverless-node-01 serverless-node-02 serverless-node-03 serverless-node-04 serverless-node-05"
app="FaaSWorkflow"

bash fetch_remote_results.sh HashCache $app $remote_hosts

bash fetch_remote_results.sh FaaSCache $app $remote_hosts

bash fetch_remote_results.sh OpenWhisk $app $remote_hosts