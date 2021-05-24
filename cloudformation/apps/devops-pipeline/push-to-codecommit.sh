#!/bin/bash

echo "Copying local files into the sync directory"
rm cloudformation/apps/data-app-code/images/covers/*.jpg
rm cloudformation/apps/devops-pipeline/data-app/*
cp -R cloudformation/apps/data-app-code/ cloudformation/apps/devops-pipeline/data-app

echo "Pushing changes into master branch"
cd cloudformation/apps/devops-pipeline/data-app/
git add .
git commit -m "pushing scripts"
git push origin master 
git push origin 
cd ../../../..