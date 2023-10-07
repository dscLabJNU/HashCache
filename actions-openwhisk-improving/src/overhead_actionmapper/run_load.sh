strategy=$1
num_input_pairs=$2

python3 generate_inputs.py --num_input_pairs $num_input_pairs
mkdir -p ./logs
locust --config=locust.conf --csv ./logs/actionMapper_overhead