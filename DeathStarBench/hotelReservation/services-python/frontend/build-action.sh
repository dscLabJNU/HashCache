#!/bin/bash

set -e
#########################################
actionName="frontend"
requestMethod="post"
basePath="/hotelReservation" 
APIPath="/$actionName"
mainfile="__main__.py"
runtime=$1
if [ -z "$runtime" ]; then
  runtime="python:3"
fi
#########################################


if [ -f "requirements.txt" ]; then
  virtualenv virtualenv
  source virtualenv/bin/activate 
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  # Zip the Python files and the installed packages.
  zip -r $actionName.zip $mainfile virtualenv
fi




wsk -i action update $actionName $actionName.zip --kind $runtime --web true --timeout 300000 --memory 1024 --annotation compute_cache True
echo $(wsk action get $actionName --url -i)
wsk api create $basePath $APIPath $requestMethod $actionName --response-type json -i