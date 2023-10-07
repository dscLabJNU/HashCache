# #!/bin/bash

# Fetch the logs
kubectl logs -n openwhisk owdev-controller-1 | grep CacheHitRate > hit_rate1.txt &
kubectl logs -n openwhisk owdev-controller-0 | grep CacheHitRate > hit_rate2.txt &
wait

# Combine the log files
cat hit_rate1.txt hit_rate2.txt > combined_hit_rate.txt

# Create the CSV file and write the header
echo "cache_hitrate" > hit_rate.csv

echo "Parse the log and write to the CSV"
# awk -F '[,:]' '{print $4 "," $5 "," $6}' combined_log.txt >> output.csv
awk -F'CacheHitRate: ' '{print $2}' combined_hit_rate.txt  >> hit_rate.csv



# Clean up the log files
rm hit_rate1.txt hit_rate2.txt combined_hit_rate.txt
