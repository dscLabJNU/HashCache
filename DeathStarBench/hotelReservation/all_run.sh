#!/bin/bash
set -e
function prune_env(){
    helm uninstall owdev -n openwhisk
}
prune_env
bash run_openwhisk.sh FaaSCache
prune_env
bash run_openwhisk.sh HashCache
prune_env
bash run_openwhisk.sh OpenWhisk