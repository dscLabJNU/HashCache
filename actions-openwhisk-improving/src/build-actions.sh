workflows=("MLWorkflow" "prediction-pipeline") # Workflow 'set_computation' is built through manifest.yaml
strategy=$1
for workflow in ${workflows[@]}
do
    cd $workflow
    bash build-actions.sh $strategy
    echo "build functions of "$workflow" successful!"
    cd ..
done

if [ "$strategy" == "HashCache" ]; then
    export AI_RUNTIME="python-io:ai"
    export NOR_RUNTIME="python-io:3"
else
    export AI_RUNTIME="python:ai"
    export NOR_RUNTIME="python:3"
fi
echo "Adding Sequence Actions, Please wait a second"
envsubst < manifest.yaml > manifest_temp.yaml
wskdeploy -m manifest_temp.yaml