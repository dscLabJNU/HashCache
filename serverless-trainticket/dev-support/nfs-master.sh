set -x
set -e

sudo apt install nfs-kernel-server

sudo systemctl enable nfs-kernel-server
sudo systemctl start nfs-kernel-server

SHARED_DIR="/var/nfs/data"
MASTER_IP=172.10.8.101


sudo mkdir $SHARED_DIR -p
sudo chmod 755 $SHARED_DIR
sudo chown vagrant $SHARED_DIR

sudo bash -c "cat >> /etc/exports << EOF 
$SHARED_DIR     172.10.8.0/24(rw,sync,no_root_squash,no_all_squash,no_subtree_check)
EOF"

sudo systemctl restart nfs-kernel-server
sudo exportfs -a

showmount -e localhost