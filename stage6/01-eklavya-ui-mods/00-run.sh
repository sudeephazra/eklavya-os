#!/bin/bash -e

on_chroot << EOF
apt-get update
apt-get -y dist-upgrade
apt-get clean
EOF

#Disable autologin
log "Disabling auto-login"
on_chroot << EOF
sed -i 's+^autologin-user=+#autologin-user=+' /etc/lightdm/lightdm.conf
EOF


