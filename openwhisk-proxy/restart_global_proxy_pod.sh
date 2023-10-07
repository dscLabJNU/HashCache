#!/bin/bash

# 获取输入的pod名字的一部分
name="hashcache-global-proxy"
deployment="hashcache-global-proxy"

strategy=$1

if [ "$strategy" != "HashCache" ] && [ "$strategy" != "FaaSCache" ] && [ "$strategy" != "OpenWhisk" ]; then
  echo "ERROR! strategy only can be [HashCache, FaaSCache, OpenWhisk]"
  exit 1
fi

# 查找匹配的pod
pods=$(kubectl get pods | grep $name | awk '{print $1}')

# 如果没有匹配的pod，输出错误信息并退出
if [ -z "$pods" ]; then
  echo "没有找到匹配的pod"
  bash apply-proxy-deployment.sh
fi

# 循环重启每个匹配的pod
for pod in $pods; do
  echo "重启pod: $pod"
  kubectl delete pod $pod
done

export STRATEGY=$strategy
envsubst < hashcache-serverless-proxy-deployment.yml | kubectl apply -f -
new_pod=$(kubectl get pods | grep $name | awk '{print $1}')
echo "新Pod: ${new_pod}"