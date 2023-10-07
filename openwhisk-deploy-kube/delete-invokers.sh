#!/bin/bash

# 获取输入的pod名字的一部分
name="invoker"

# 查找匹配的pod
pods=$(kubectl get pods -n openwhisk| grep $name | awk '{print $1}')

# 如果没有匹配的pod，输出错误信息并退出
if [ -z "$pods" ]; then
  echo "没有找到匹配的pod"
  exit 1
fi

# 循环重启每个匹配的pod
for pod in $pods; do
  echo "删除pod: $pod"
  kubectl delete pod -n openwhisk $pod &
done
wait
echo "删除完成"
