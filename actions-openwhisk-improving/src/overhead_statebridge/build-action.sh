#!/bin/bash
#########################################
actionName="blob_cache"
requestMethod="post"
basePath="/overhead" 
APIPath="/blob_cache"
mainfile="__main__.py"
runtime=$1
if [ -z "$runtime" ]; then
  runtime="python-io:ai"
fi
#########################################


if [ -f "requirements.txt" ]; then
  virtualenv virtualenv --python=python3.8
  source virtualenv/bin/activate
  pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  # Zip the Python files and the installed packages.
  echo "zip -r $actionName.zip $mainfile virtualenv"
  zip -r $actionName.zip $mainfile virtualenv/
else
    zip -r $actionName.zip $mainfile
fi


# 定义命令变量
cmd='wsk -i action update $actionName blob_cache.zip --kind $runtime --web true --timeout 300000 --memory 1024'

# 循环执行命令
for i in {1..5}; do
    # 替换变量
    actionName="blob_cache_$i"
    APIPath="/$actionName"
      #执行命令
    eval $(echo $cmd | sed "s/\$actionName/$actionName/g")
    
    # 输出 action 的 URL
    echo $(wsk action get $actionName --url -i)
    
    # 创建 API
    wsk api create $basePath $APIPath $requestMethod $actionName --response-type json -i
done