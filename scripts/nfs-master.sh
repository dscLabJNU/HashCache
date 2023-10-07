#!/bin/bash

MASTER_IP="172.10.8.101"
SHARED_DIR="/var/nfs/data"

# Install NFS server
sudo apt update -y
sudo apt install -y nfs-kernel-server

# Start rpcbind service
sudo systemctl start rpcbind.service
sudo systemctl enable rpcbind.service

# Create shared directory
sudo mkdir -p $SHARED_DIR
sudo chown nobody:nogroup $SHARED_DIR
sudo chmod 777 $SHARED_DIR

# Check if the exports file contains the shared directory
if grep -qs $SHARED_DIR /etc/exports; then
  echo "The exports file already contains the shared directory."
else
  # Configure NFS exports
  sudo sh -c "echo '$SHARED_DIR 172.10.8.0/24(rw,sync,no_root_squash,no_all_squash,no_subtree_check)' >> /etc/exports"
  sudo exportfs -a
fi

# Restart NFS server
sudo systemctl restart nfs-kernel-server

showmount -e localhost

