remote_hosts="serverless-node-01 serverless-node-02 serverless-node-03 serverless-node-04 serverless-node-05"

bash fetch_remote_results.sh HashCache hotelReservation $remote_hosts

bash fetch_remote_results.sh FaaSCache hotelReservation $remote_hosts

bash fetch_remote_results.sh OpenWhisk hotelReservation $remote_hosts