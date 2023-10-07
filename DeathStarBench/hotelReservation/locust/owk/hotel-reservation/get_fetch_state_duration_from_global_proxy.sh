# 获取输入的pod名字的一部分
name="hashcache-global-proxy"

# 查找匹配的pod
pods=$(kubectl get pods | grep $name | awk '{print $1}')

# 如果没有匹配的pod，输出错误信息并退出
if [ -z "$pods" ]; then
  echo "没有找到匹配的pod"
  exit 1
fi
echo "fetch_time(s)" > fetch_state.csv
# 循环重启每个匹配的pod
for pod in $pods; do
  kubectl logs $pod | grep -o 'tooks [0-9.]* seconds' | awk '{print $2}' >> fetch_state.csv
done