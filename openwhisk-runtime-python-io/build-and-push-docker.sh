#!/bin/bash

set -e
function push_image(){
    echo "Pushing docker image with suffix: $strategy"
    strategy=$1
    docker push diomwu/action-python-io-v3.7:$strategy
    docker push diomwu/action-python-io-v3.6-ai:$strategy
}

function build(){
    echo "Building docker image of strategy: $strategy"
    ./gradlew core:python36AiAction:distDocker  &
    ./gradlew core:python3Action:distDocker &
    wait
}

function update_launcher_gradle(){
    strategy=$1
    echo "Updating launcher.py to strategy: $strategy"
    
    cp gradle/docker_$strategy.gradle gradle/docker.gradle
    case "$strategy" in
    HashCache)
        cp core/python3Action/lib/launcher_improving.py core/python3Action/lib/launcher.py
        ;;
    FaaSCache)
        cp core/python3Action/lib/launcher_caching.py core/python3Action/lib/launcher.py
        ;;
    OpenWhisk)
        cp core/python3Action/lib/launcher_caching.py core/python3Action/lib/launcher.py
        ;;
    esac

}

function go(){
    strategy=$1
    update_launcher_gradle $strategy
    build
    push_image $strategy
}

strategy="$1"
case "$strategy" in
  HashCache)
    go $strategy
    ;;
  FaaSCache)
    go $strategy
    ;;
  OpenWhisk)
    go $strategy
    ;;
  *)
    echo "Invalid strategy: $strategy"
    echo "Usage: $0 [HashCache, FaaSCache, OpenWhisk]"
    exit 1
    ;;
esac