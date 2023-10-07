#!/bin/bash

MASTER_IP="172.10.8.101"
SHARED_DIR="/var/nfs/data"

# Install NFS client
sudo apt update -y
sudo apt install -y nfs-common


# Start rpcbind service
sudo systemctl restart rpcbind.service
sudo systemctl enable rpcbind.service


# Delete busy process and umount
# sudo fuser -m -v -k $SHARED_DIR
sudo umount -f $SHARED_DIR
sudo rm -rf $SHARED_DIR


# Create mount point
sudo mkdir -p $SHARED_DIR

# Unmount any existing NFS at the mount point
sudo umount -f $SHARED_DIR || true

# Mount shared directory from master
sudo mount -t nfs $MASTER_IP:$SHARED_DIR $SHARED_DIR

# Add mount entry to /etc/fstab for auto-mount on boot
if grep -qs $SHARED_DIR /etc/fstab; then
  echo "The fstab file already contains the mount entry."
else
  echo "$MASTER_IP:$SHARED_DIR $SHARED_DIR nfs auto,nofail,noatime,nolock,intr,tcp,actimeo=1800 0 0" | sudo tee -a /etc/fstab
fi

mount | grep $MASTER_IP
