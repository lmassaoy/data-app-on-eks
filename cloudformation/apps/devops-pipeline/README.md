# Building the DevOps Pipeline

## Pre-Reqs

- Docker Hub credentials

## CloudFormation execution to build the cloud components
```
$ aws cloudformation deploy \
    --template-file cloudformation/apps/devops-pipeline/devops-pipeline.yaml \
    --stack-name data-app-devops-pipeline \
    --capabilities CAPABILITY_NAMED_IAM \
    --tags ProjectName=DataAppOnEKS
```

**Important**

In order to clone the repository, you should set up your GIT credentials (https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-gc.html). Make sure you already have them before proceeding.

Run the following command to clone the CodeCommit Repository into your local repo.
```
$ sh cloudformation/apps/devops-pipeline/git-clone.sh
```

Now let's copy the scripts of our Data App into the repository and push them into the CodeCommit Repository
```
$ sh cloudformation/apps/devops-pipeline/push-codecommit-repo.sh
```

Building the image locally with Docker
```
$ docker build -t data-app/data-app:latest -f cloudformation/apps/data-app-code/Dockerfile .
```

TODO IaC:
- CodeBuild + Service Role (SSM & KMS permissions + ECR permissions)
- CodePipeline
- KMS key for docker credentials
- Docker credentials
- SSM Parameters
    - DOCKER HUB CREDENTIALS