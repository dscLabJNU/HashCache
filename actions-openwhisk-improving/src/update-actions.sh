echo "Adding Sequence Actions, Please wait a second"
strategy=$1
if [ "$strategy" == "HashCache" ]; then
    export AI_RUNTIME="python-io:ai"
    export NOR_RUNTIME="python-io:3"
else
    export AI_RUNTIME="python:ai"
    export NOR_RUNTIME="python:3"
fi
envsubst < manifest.yaml > manifest_temp.yaml
wskdeploy -m manifest_temp.yaml

# cd FINRA/compose
# bash build-FINRA.sh
# cd -