# Build your own Amazon EKS cluster

## Pre-reqs:

- eksctl (version >= 0.50.0)
    - https://eksctl.io/introduction/
- kubectl (latest)
- AWS CLI already configured (version >= 2.1.6)


## Step-by-Step

1. Creating the cluster

    Running the following command creates a stack at CloudFormation that will build the Amazon EKS clusters using AWS Fargate profiles:

    Option A - with config file
    ```
    $ eksctl create cluster -f cloudformation/infra/eks-cluster/eks-cluster.yaml
    ```
    Option B - simpler version
    ```
    $ eksctl create cluster \
        --region us-east-1 \
        --name data-apps-cluster \
        --fargate \
        --tags ProjectName=DataAppOnEKS
    ```
    *Note that the process may take several minutes (around 30)*


2. Testing the configuration using kubectl

    Running the following command:
    ```
    $ kubectl get svc
    ```
    should get an output like this:
    ```
    NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
    kubernetes   ClusterIP   172.20.0.1   <none>        443/TCP   31m
    ```
    This means you're ready to start using the EKS cluster.

3. Create a Fargate Profile which will be used with the applications soon, and a Namespace named as "data-apps":
    
    Create a new Fargate Profile for the Namespace: "data-apps":

    Create the Namespace:

    ```
    $ kubectl create namespace data-apps
    ```
    
    **Skip the following command if you chosed the Option 1.A**

    ```
    $ eksctl create fargateprofile --namespace data-apps --cluster kube-cluster --name fp-data-apps
    ```

## Optional Tasks - Cluster Monitoring Tools
1. Setup the Kubernetes Metrics Server
    - https://docs.aws.amazon.com/eks/latest/userguide/metrics-server.html

2. Setup Kubernetes Dashboard (this task needs the Kubernetes Metrics Server running)
    - https://docs.aws.amazon.com/eks/latest/userguide/dashboard-tutorial.html

3. Setup Prometheus + Grafana
    - install Helm: https://docs.aws.amazon.com/eks/latest/userguide/helm.html
    - add a nodegroup (Prometheus' deployments need EBS volumes in order to work properly):
        ```
        $ eksctl create nodegroup --config-file=cloudformation/infra/eks-cluster/prometheus-ng.yaml
        ```
    - https://www.eksworkshop.com/intermediate/240_monitoring/