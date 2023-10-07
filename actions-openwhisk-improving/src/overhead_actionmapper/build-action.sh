#!/bin/bash
#########################################
actionName="huge_input_output"
requestMethod="post"
basePath="/overhead" 
APIPath="/huge_input_output"
mainfile="__main__.py"
runtime=$1
if [ -z "$runtime" ]; then
  runtime="python:3"
fi
#########################################

# 定义命令变量
cmd='wsk -i action update $actionName $mainfile --kind $runtime --web true --timeout 300000 --memory 1024'

# 循环执行命令
for i in {1..20}; do
    # 替换变量
    actionName="huge_input_output_$i"
    APIPath="/$actionName"
      #执行命令
    eval $(echo $cmd | sed "s/\$actionName/$actionName/g")
    
    # 输出 action 的 URL
    echo $(wsk action get $actionName --url -i)
    
    # 创建 API
    wsk api create $basePath $APIPath $requestMethod $actionName --response-type json -i
done