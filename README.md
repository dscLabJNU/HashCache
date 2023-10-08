# HashCache

## Introduction

HashCache is a caching framework designed to enhance the efficiency of serverless computing platforms by avoiding duplicate function executions.

The core concept behind HashCache is to cache the computational results of annotated functions. This enables the framework to quickly provide pre-computed results for subsequent invocations of the same functions, thereby skipping the need for duplicate computations.

In addition to caching computational results, HashCache leverages the infrequent updates typically observed in cloud storage objects. It not only caches the computational results of stateful functions by monitoring changes in associated remote blobs, but also caches the most recent versions of these remote blobs to improve data retrieval efficiency.



HashCache has been accepted by TPDS (Transactions on Parallel and Distributed Systems).

If you use HashCache in your research, please cite our TPDS paper:

```
Comming soon
```



## Getting Started

### 0. Clone the repository

```
git clone https://github.com/dscLabJNU/HashCache.git
```

### 1. NFS cluster

In your master node, modify `MASTER_IP` and the CIDR in line 24, then run `bash nfs-master.sh`
In all worker nodes, adjust `MASTER_IP` then run `bash nfs-worker.sh`

### 2. Basic environments

```shell
# Install Python3.8 and pip3 by yourself
cd scripts
pip3 install -r requirements.txt
```

#### 2.1. Other dependencies:

```shell
bash java_and_maven.sh
bash node12.sh
sudo apt-get install -y jq unzip zip

# install gradle
wget -c https://services.gradle.org/distributions/gradle-5.5.1-bin.zip -P /tmp
sudo unzip -d /opt/gradle /tmp/gradle-5.5.1-bin.zip
# Write into ~/.bashrc
export GRADLE_HOME=/opt/gradle/gradle-5.5.1
export PATH=${GRADLE_HOME}/bin:${PATH}
source ~/.bashrc 

# install helm
tar -zxvf helm-v3.8.0-linux-amd64.tar.gz
sudo mv linux-amd64/helm /usr/local/bin/
rm -rf linux-amd64

# install wskdeploy
wget -c https://github.com/apache/openwhisk-wskdeploy/releases/download/1.2.0/openwhisk_wskdeploy-1.2.0-linux-amd64.tgz -P /tmp
tar -zxvf /tmp/openwhisk_wskdeploy-1.2.0-linux-amd64.tgz
sudo mv /tmp/wskdeploy /usr/local/bin/


# Make sure that all nodes in the cluster can communicate password-free SSH with each othe, follwing are our `/etc/hosts` settings in each node:
172.10.8.101 serverless-node-01
172.10.8.102 serverless-node-02
172.10.8.103 serverless-node-03
172.10.8.104 serverless-node-04
172.10.8.105 serverless-node-05
```

#### 2.2. Install OpenWhisk-cli

```shell
wget https://github.com/apache/openwhisk-cli/releases/download/1.2.0/OpenWhisk_CLI-1.2.0-linux-amd64.tgz
tar -zxvf OpenWhisk_CLI-1.2.0-linux-amd64.tgz wsk
sudo mv wsk /usr/local/bin

# Set wsk-cli properties
wsk property set --apihost 172.17.8.101:31001
wsk property set --auth 23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP
```

### 3. Run OpenWhisk

```shell
# Set invoker rule so they can lauch `owddev-invoker` pods
kubectl label nodes serverless-node-02 serverless-node-03 serverless-node-04 serverless-node-05 openwhisk-role=invoker

cd openwhisk-deploy-kube
bash swiching_openwhisk_version.sh [OpenWhisk | FaaSCache | HashCache]
```

Run `kubectl get pod -n openwhisk -o wide` and wait the STATUS of `owdev-install-packages` changes to `Completed`.
It may take some time (10 mins?).

### 4. Setting the configurable parameters

#### 4.1. AWS account
Checkout the `__main__.py` in `actions-openwhisk-improving/src/*`, and set your `aws_access_key_id` and `aws_secret_access_key`.

#### 4.2. Resource Monitor
Check and modify the parameters in `paramaters.json` under the `openwhisk-resource-monitor` folder.
Run `bash monitor_resources.sh` to make sure the script is ready.


### 5. Experimental results:

Run `bash all_run.sh` in `action-openwhisk-improving`, `DeathStartBench/hotalREservation` and `serverless-trainticket` folders.

If all goes right, the experimental results will be stored at the corresponding folders.


#### 5.1. FaaSWorkflow:

For `FaaSWorkflow`, the experimental results will be stored at `actions-openwhisk-improving/load-gen/locust/logs`.

#### 5.2. HotelReservation:

HotelReservation's results will be shown at `DeathStarBench/hotelReservation/locust/owk/hotel-reservation/logs`.

#### 5.3. TrainTicket:

The experimental results of ServerlessTrainTicket application could be found at `serverless-trainticket/src/load-gen/logs/`