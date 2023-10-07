<!--
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
-->

# Deploying OpenWhisk on IBM Cloud Kubernetes Service (IKS)

## Overview

IBM provides both a "Lite" and a "Standard" Kubernetes offering in its
public cloud Kubernetes service (IKS). These differ in capabilities,
so they are described separately below.

## Initial setup

### Creating the Kubernetes Cluster

Follow IBM's instructions to provision your cluster.

### Configuring OpenWhisk

####  IBM Cloud Standard cluster

An IBM Cloud Standard cluster has full support for TLS
including a wild-card certificate for subdomains
and can be configured with additional annotations to
fine tune ingress performance.

First, determine the values for <domain> and <ibmtlssecret> for
your cluster by running the command:
```
ibmcloud cs cluster get -c <mycluster>
```
The CLI output will look something like
```
ibmcloud cs cluster get -c <mycluster>
Retrieving cluster <mycluster>...
OK
Name:    <mycluster>
...
Ingress Subdomain:  <domain>
Ingress Secret:     <ibmtlssecret>
...
```

As described in [IBM's ingress documentation](https://cloud.ibm.com/docs/containers/cs_ingress.html#ingress),
to enable applications deployed in multiple namespaces to share the ingress resource,
you should use a unique subdomain name for each namespace.  We suggest
a convention of using the namespace name as the subdomain name.  So if you
are deploying openwhisk into the `openwhisk` namespace, use `openwhisk`
as your subdomain (as shown below in the example `mycluster.yaml`).

A template [mycluster.yaml](../deploy/ibm-public/mycluster-iks.yaml]
for a standard deployment of OpenWhisk on IKS would be:
```yaml
whisk:
  ingress:
    # NOTE: Replace <domain> with your cluster's actual domain
    apiHostName: openwhisk.<domain>
    apiHostPort: 443
    apiHostProto: https
    type: Standard
    useInternally: true
    # NOTE: Replace <domain> with your cluster's actual domain
    domain: openwhisk.<domain>
    tls:
      enabled: true
      secretenabled: true
      createsecret: false
      # NOTE: Replace <ibmtlssecret> with your cluster's actual tlssecret
      secretname: <ibmtlssecret>
    annotations:
      kubernetes.io/ingress.class: public-iks-k8s-nginx
      nginx.ingress.kubernetes.io/use-regex: "true"
      nginx.ingress.kubernetes.io/configuration-snippet: |
         proxy_set_header X-Request-ID $request_id;
      nginx.ingress.kubernetes.io/proxy-body-size: 50m
      nginx.ingress.kubernetes.io/proxy-read-timeout: "75"

invoker:
  containerFactory:
    impl: kubernetes
```

The underlying container runtime used by IKS is containerd.
Therefore, you cannot use the DockerContainerFactory on IKS and must
use the KubernetesContainerFactory.

####  IBM Cloud Lite cluster

The only available ingress method for an IBM Cloud Lite cluster is to
use a NodePort. Obtain the Public IP address of the sole worker node
by using the command
```shell
ibmcloud cs workers <my-cluster>
```
Then define `mycluster.yaml` as
```yaml
whisk:
  ingress:
    type: NodePort
    apiHostName: YOUR_WORKERS_PUBLIC_IP_ADDR
    apiHostPort: 31001
    useInternally: true

nginx:
  httpsNodePort: 31001

# disable affinity
affinity:
  enabled: false
toleration:
  enabled: false
invoker:
  options: "-Dwhisk.kubernetes.user-pod-node-affinity.enabled=false"
  # must use KCF as IKS uses containerd as its container runtime
  containerFactory:
    impl: "kubernetes"
```

## Hints and Tips

On IBM Standard clusters, you can configure OpenWhisk to integrate
with platform logging and monitoring services following the general
instructions for enabling these services for pods deployed on
Kubernetes.

## Limitations

Using an IBM Cloud Lite cluster is only appropriate for development
and testing purposes.  It is not recommended for production
deployments of OpenWhisk.

When using an IBM Cloud Lite cluster, TLS termination will be handled
by OpenWhisk's `nginx` service and will use self-signed certificates.
You will need to invoke `wsk` with the `-i` command line argument to
bypass certificate checking.
