#!/bin/bash
bash delete-all-pv.sh
cd ../deployment/Part01-database/
kubectl delete -f ts-serverless-database-deployment.yml
kubectl delete -f ts-serverless-persistent-deployment.yml
sudo rm -rf /var/nfs/data/*
cd -

cd ../deployment/Part02-backend/service/
kubectl delete -f ts-serverless-service-deployment.yml
cd -

cd ../deployment/Part03-frontend/
kubectl delete -f ts-serverless-frontend-deployment.yml