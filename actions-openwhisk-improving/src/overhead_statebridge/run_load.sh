strategy=$1

mkdir -p ./logs/$strategy
locust --config=locust.conf --csv ./logs/$strategy/stateBridge_overhead