#!/bin/bash
cd ../
./part01_DataBaseDeployment_owk.sh
cd -

cd ../deployment/Part02-backend/service/
kubectl apply -f ts-serverless-service-deployment.yml
cd -

cd ../deployment/Part03-frontend/
kubectl apply -f ts-serverless-frontend-deployment.yml