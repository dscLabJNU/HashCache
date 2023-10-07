# #!/bin/bash

# 获取输入的pod名字的一部分
name="owdev-invoker"

# 查找匹配的pod
pods=$(kubectl get pods -n openwhisk | grep -E ^$name | awk '{print $1}')
log_file="duplicate_execution_log.csv"

# 如果没有匹配的pod，输出错误信息并退出
if [ -z "$pods" ]; then
  echo "没有找到匹配的pod"
  exit 1
fi
echo $pods
echo "func_name,hash_input,hash_output,duration(ms)" > $log_file
# 循环重启每个匹配的pod
for pod in $pods; do
    kubectl logs -n openwhisk $pod | grep "\[Invocation Done\]" | awk -F '[,:]' '{gsub(/ /, "", $4); sub(/ milliseconds/, "", $7); print $4 "," $5 "," $6 "," $7}' >> $log_file
done