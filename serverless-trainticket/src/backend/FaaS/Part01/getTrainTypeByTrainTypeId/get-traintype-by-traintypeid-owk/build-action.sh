set -e
gradle clean
gradle shadowJar

#########################################
actionName="get-traintype-by-traintypeid"
requestMethod="get" 
basePath="/traintype" 
APIPath="/getTrainTypeByTrainTypeId"
param="/{trainTypeId}"
runtime=$1
if [ -z "$runtime" ]; then
  runtime="java:8-io"
fi
echo "JAVA_RUNTIME $runtime"
#########################################

wsk -i action update $actionName ./build/libs/function.jar --main Handler --kind $runtime --web true --timeout 300000 --memory 1024 --annotation compute_cache True # timeout 300s
echo $(wsk action get $actionName --url -i)
wsk api create $basePath $APIPath$param $requestMethod $actionName --response-type http -i