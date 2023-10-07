set -e
echo "Part01 DataBase Deployment"

mkdir /var/nfs/data/station -p
mkdir /var/nfs/data/auth -p
mkdir /var/nfs/data/config -p
mkdir /var/nfs/data/contacts -p
mkdir /var/nfs/data/insidePayment -p
mkdir /var/nfs/data/order -p
mkdir /var/nfs/data/payment -p
mkdir /var/nfs/data/price -p
mkdir /var/nfs/data/route -p
mkdir /var/nfs/data/security -p
mkdir /var/nfs/data/train -p
mkdir /var/nfs/data/travel -p
mkdir /var/nfs/data/user -p
 

cd deployment/Part01-database/
# kubectl delete -f ts-serverless-database-deployment.yml
kubectl apply -f ts-serverless-database-deployment.yml

# kubectl delete -f ts-serverless-persistent-deployment.yml
kubectl apply -f ts-serverless-persistent-deployment.yml
cd ../..
echo "Part1 DataBase deployment finished"
