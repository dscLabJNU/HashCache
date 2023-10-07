echo "Part03 Front Deployment"
cd src/frontend
bash build-image.sh
cd -
cd deployment/Part03-frontend/
kubectl delete -f ts-serverless-frontend-deployment.yml
kubectl create -f ts-serverless-frontend-deployment.yml

cd ..
cd ..

echo "Done"