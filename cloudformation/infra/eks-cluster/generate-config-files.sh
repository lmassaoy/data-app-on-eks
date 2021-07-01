#!/bin/bash

IFS=','

joinByChar() {
  echo "$*"
}

if [ -z "$AWS_ACCOUNT" ]; then
  echo "Environment variable AWS_ACCOUNT not exists or is empty."
  exit 0;
fi

while getopts r:z: flag
do
    case "${flag}" in
        r) REGION=${OPTARG};;
        z) AZS=${OPTARG};;
        *) exit
    esac
done

AVAILABILITY_ZONES_LIST=()
read -r -a AZS <<< "$AZS"
for az in "${AZS[@]}";
do
   AVAILABILITY_ZONES_LIST+=(\""$az"\")
done

AVAILABILITY_ZONES=$(joinByChar "${AVAILABILITY_ZONES_LIST[*]}")

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
            "Resource": [
              "arn:aws:s3:::anime-bucket-$AWS_ACCOUNT-$REGION/*",
              "arn:aws:s3:::anime-bucket-$AWS_ACCOUNT-$REGION"
            ]
        }
    ]
}
EOF

cat <<EOF >cloudformation/infra/eks-cluster/data-apps-cluster.yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: data-apps
  region: $REGION
  tags:
    ProjectName: DataAppOnEKS

nodeGroups:
  - name: kubernetes-management-services-ng
    instanceType: t4g.medium
    desiredCapacity: 1
    volumeSize: 40
    privateNetworking: true
    availabilityZones: [$AVAILABILITY_ZONES]

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