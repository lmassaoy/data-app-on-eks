# Building the Storage for the Dataset

## Pre-Reqs

- AWS CLI

## CloudFormation execution to build the cloud components
```
$ aws cloudformation deploy \
    --template-file cloudformation/infra/dataset-storage/dataset-storage.yaml \
    --stack-name data-app-object-store \
    --capabilities CAPABILITY_NAMED_IAM \
    --tags ProjectName=DataAppOnEKS
```

## Sending the datasets into the S3 bucket
```
$ BUCKET_NAME=$(aws cloudformation --region us-east-1 describe-stacks --stack-name data-app-object-store --query "Stacks[0].Outputs[?OutputKey=='AnimeBucketName'].OutputValue" --output text)

$ aws s3 cp --recursive dataset/ s3://$BUCKET_NAME/
```