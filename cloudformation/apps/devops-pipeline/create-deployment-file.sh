#!/bin/bash

cat <<EOF >cloudformation/apps/devops-pipeline/deployment.yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  namespace: data-apps
  name: deployment-data-apps
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: data-app
  replicas: 3
  template:
    metadata:
      labels:
        app.kubernetes.io/name: data-app
    spec:
      serviceAccountName: data-apps-service-account
      containers:
      - image: $AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/data-app-on-eks:latest
        imagePullPolicy: Always
        name: data-app
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1024Mi"
            cpu: "1000m"
        env:
          - name: BUCKET_NAME
            value: $(aws cloudformation --region us-east-1 describe-stacks --stack-name data-app-object-store --query "Stacks[0].Outputs[?OutputKey=='AnimeBucketName'].OutputValue" --output text)
          - name: GENRES_FILE
            value: animes_genres.parquet
          - name: ANIME_FILE
            value: prepared_animes.parquet
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  namespace: data-apps
  name: data-apps-on-eks
spec:
  ports:
    - port: 80
      targetPort: 80
      protocol: TCP
  type: LoadBalancer
  selector:
    app.kubernetes.io/name: data-app
EOF