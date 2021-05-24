#!/bin/bash

cat <<EOF >cloudformation/infra/eks-cluster/read-write-s3-policy-doc.json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:GetBucketVersioning",
                "s3:DeleteObject"
            ],
            "Resource": "arn:aws:s3:::anime-bucket-$AWS_ACCOUNT-us-east-1/*"
        }
    ]
}
EOF

cat <<EOF >cloudformation/infra/eks-cluster/data-apps-cluster.yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: data-apps
  region: us-east-1
  tags:
    ProjectName: DataAppOnEKS

nodeGroups:
  - name: kubernetes-management-services-ng
    instanceType: t4g.medium
    desiredCapacity: 1
    volumeSize: 40
    privateNetworking: true

fargateProfiles:
  - name: fp-default
    selectors:
      - namespace: default
      - namespace: kube-system
    tags:
      ProjectName: DataAppOnEKS
  - name: fp-data-apps
    selectors:
      - namespace: data-apps
    tags:
      ProjectName: DataAppOnEKS

iam:
  withOIDC: true
  serviceAccounts:
  - metadata:
      name: data-apps-service-account
      namespace: data-apps
    attachPolicyARNs:
    - "arn:aws:iam::$AWS_ACCOUNT:policy/ReadWriteAnimeBucketObjects"
    tags:
      ProjectName: DataAppOnEKS

cloudWatch:
    clusterLogging:
        enableTypes: ["*"]
EOF