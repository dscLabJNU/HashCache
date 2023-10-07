set -e
gradle clean
gradle shadowJar

#########################################
actionName="init-contacts-mongo"
requestMethod="post" 
basePath="/initDB" 
APIPath="/initContactsMongo"
runtime=$1
if [ -z "$runtime" ]; then
  runtime="java:8-io"
fi
echo "JAVA_RUNTIME $runtime"
#########################################

wsk -i action update $actionName ./build/libs/function.jar --main Handler --kind $runtime --web true --timeout 300000 --memory 1024 # timeout 300s
echo $(wsk action get $actionName --url -i)
wsk api create $basePath $APIPath $requestMethod $actionName --response-type json -i