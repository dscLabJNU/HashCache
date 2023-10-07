# #!/bin/bash
echo "Getting function-input-output logs from owk controllers..."
# Fetch the logs
kubectl logs -n openwhisk owdev-controller-1 | grep Redundant > log1.txt &
kubectl logs -n openwhisk owdev-controller-0 | grep Redundant > log2.txt &
wait

# Combine the log files
cat log1.txt log2.txt > combined_log.txt

# Create the CSV file and write the header
echo "func_name,hash_input,hash_output" > function_input_output_log.csv

awk -F '[,:]' '{gsub(/ /, "", $4); print $4 "," $5 "," $6}' combined_log.txt >> function_input_output_log.csv



# Clean up the log files
rm log1.txt log2.txt combined_log.txt
