#!/bin/bash

# 获取所有的container id
container_ids=$(docker ps | grep social-network-microservice | awk '{print $1}')
output_files=()
log_file="duplicate_execution_log.csv"
# 为每个container id启动一个子进程
for id in $container_ids
do
    output_file="output_${id}.csv"
    output_files+=($output_file)
    # 使用awk获取需要的信息并输出到CSV文件，这是一个后台进程
    docker logs $id 2>&1 | grep 'FunctionLog' | sed 's/\[FunctionLog\]: //' > $output_file &
done

# 等待所有的子进程完成
wait



# 合并所有的CSV文件到一个文件
echo "func_name,hash_input,hash_output,duration(s)" > $log_file
for file in "${output_files[@]}"
do
    # 删除包含"FunctionLog"的行
    sed -i '/FunctionLog/d' $file
    
    tail -n +2 $file >> $log_file
    rm $file
    sleep 0.1
done
awk -F',' 'NF<5' $log_file > file_filtered.csv
mv file_filtered.csv $log_file

bash filter_function_logs.sh