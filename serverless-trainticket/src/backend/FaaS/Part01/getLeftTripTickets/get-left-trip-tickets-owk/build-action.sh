set -e
gradle clean
gradle shadowJar
#########################################
actionName="get-left-trip-tickets"
requestMethod="post" 
basePath="/tickets" 
APIPath="/getLeftTripTickets"
runtime=$1
if [ -z "$runtime" ]; then
  runtime="java:8-io"
fi
echo "JAVA_RUNTIME $runtime"
#########################################

wsk -i action update $actionName ./build/libs/function.jar --main Handler --kind $runtime --web true
echo $(wsk action get $actionName --url -i)
wsk api create /tickets  /getLeftTripTickets post $actionName --response-type json -i