# Serverless TrainTicket

[TrainTicket](https://github.com/FudanSELab/train-ticket) 是复旦大学 CodeWisdom 团队按照工业界微服务实践所开发的一个开源微服务基准系统，是基于微服务架构的一个火车订票系统，包含了 41 种微服务。本项目使用开源函数计算框架 OpenFaaS、基于 Serverless 架构提取并改造开源微服务系统 TrainTicket 中高并发的订票业务，部署并运行在 Kubernetes 集群中。主要使用的开发技术框架如下：

- Java - OpenFaaS、OkHttp、*Spring Boot
- DB - MongoDB、MongoBD JDBC



## 快速开始

本项目基于 Kubernetes 集群并使用开源函数计算框架 OpenFaaS 来部署我们的 Serverless TrainTicket 系统。

### 先决条件

由于本项目选择Kubernetes 来构建 OpenFaaS 的 Serverless 平台，因此你需要至少两台服务器以构建 Kubernetes 集群。[集群部署教程](https://blog.csdn.net/lbw520/article/details/96446272)

#### 服务器系统要求

- CPU和内存：双核，4GB以上。
- 操作系统：基于x86_64的各种Linux发行版，包括CentOS，Federa，Ubuntu等，但内核要求在3.10及以上。
- 容器运行时：一般情况下使用Docker作为容器运行时。

### 1. 登录Docker Hub

```shell
docker login -u <username> -p <password>
```

### 2. 安装NFS

详细步骤参考[该链接](https://qizhanming.com/blog/2018/08/08/how-to-install-nfs-on-centos-7)，本项目中master节点为nfs服务端、所有node节点为nfs客户端，挂载路径为`/var/nfs/data/`。

### 2. 安装OpenFaaS

详细步骤参考[OpenFaaS官方文档](https://docs.openfaas.com/deployment/kubernetes/)。官方提供了三种安装OpenFaaS的方法，建议使用 helm（arkade不够成熟，yaml文件支持定制自定义安装方案但过于繁琐）。

### 3. 克隆项目仓库

```sh
https://github.com/dscLabJNU/serverless-trainticket-improving
```
### 4. 运行openwhisk并构建函数
```sh
bash run_openwhisk.sh [HashCache, FaaSCache, OpenWhisk]
```

### 5. 运行 `kubectl get pods --all-namespaces` 等待所有 Pods 都是 Ready 状态

### 6. 访问 Serverless TrainTicket 主页 http://[Node-IP]:32677


### 7. 其他serverless应用
安装wskdeploy https://github.com/apache/openwhisk-wskdeploy/releases
action-openhwhisk-improving
sudo npm install -g openwhisk-composer
