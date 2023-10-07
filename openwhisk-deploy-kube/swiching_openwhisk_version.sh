#!/bin/bash
set -e

# check函数用于检测openwhisk命名空间下的helm资源owdev有没有在运行
function check() {
  helm status owdev -n openwhisk >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "owdev is running"
    return 0
  else
    echo "owdev is not running"
    return 1
  fi
}

function install_owdev() {
    yaml=$1
    echo "Install openwhisk..."
    helm install owdev ./helm/openwhisk --create-namespace -n openwhisk -f $yaml >/dev/null
}


function upgrade_owdev() {
    yaml=$1
    echo "Upgrading openwhisk..."
    helm upgrade owdev ./helm/openwhisk -n openwhisk -f $yaml >/dev/null
}

function usage() {
    echo -e "Usage: $0 [HashCache, FaaSCache, OpenWhisk]"
}


if [[ $# -lt 1 ]]; then
    usage
    exit
else
    strategy=$1
    case "$strategy" in
    "HashCache" | "FaaSCache" | "OpenWhisk")
        echo "Launching OpenWhisk with strategy: $strategy"
        yaml="${strategy}Cluster.yaml"
        # 主程序逻辑，根据check函数的返回值来执行install或upgrade函数
        if check; then
          upgrade_owdev $yaml
        else
          install_owdev $yaml
        fi
        ;;
    *) # default
        usage
        exit
        ;;
    esac
fi
