#!/bin/bash

#########################################
actionName="linear_regression"
requestMethod="post"
basePath="/MLWorkflow" 
APIPath="/linear_regression"
mainfile="__main__.py"
runtime=$1
if [ -z "$runtime" ]; then
  runtime="python:ai"
fi
#########################################


if [ -f "requirements.txt" ]; then
  virtualenv virtualenv
  source virtualenv/bin/activate 
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  # Zip the Python files and the installed packages.
    zip -r $actionName.zip $mainfile virtualenv
else
    zip -r $actionName.zip $mainfile
fi



wsk -i action update $actionName $actionName.zip --kind $runtime --web true --timeout 300000 --memory 1024 --annotation compute_cache True # timeout 300s
echo $(wsk action get $actionName --url -i)
wsk api create $basePath $APIPath $requestMethod $actionName --response-type json -i