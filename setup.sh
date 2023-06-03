#!/bin/bash

# set -o xtrace

USERNAME=$(jq -r '.username' /mnt/config.json)
PASSWORD=$(jq -r '.password' /mnt/config.json)
VNCPASS=$(jq -r '.vncpasswd' /mnt/config.json)

useradd -m -s /bin/bash $USERNAME
echo "$USERNAME:$PASSWORD" | chpasswd
mkdir -p "/home/$USERNAME/.vnc"
x11vnc -storepasswd $VNCPASS /home/$USERNAME/.vnc/passwd 2>&1
chmod a+r "/home/$USERNAME/.vnc/passwd"

sudo -u $USERNAME Xvfb :99 2>&1 &
sudo -u $USERNAME DISPLAY=:99 startxfce4 2>&1 &
sudo -u $USERNAME x11vnc -forever -usepw -display :99 2>&1

