log_file="duplicate_execution_log.csv"
awk -F, 'BEGIN {OFS=FS} $1 ~ /^[a-zA-Z_]/' $log_file > temp.csv
mv temp.csv $log_file