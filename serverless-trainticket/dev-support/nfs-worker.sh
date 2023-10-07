set -x
set -e
MASTER_IP=172.10.8.101

sudo apt-get install nfs-common -y

sudo systemctl enable rpcbind
sudo systemctl start rpcbind

showmount -e $MASTER_IP
SHARED_DIR="/var/nfs/data"
sudo mkdir -p $SHARED_DIR
sudo chown vagrant $SHARED_DIR
sudo mount -t nfs $MASTER_IP:$SHARED_DIR $SHARED_DIR

mount | grep $MASTER_IP