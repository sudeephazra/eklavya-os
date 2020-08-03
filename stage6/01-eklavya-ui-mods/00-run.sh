#!/bin/bash -e

#Disable autologin
on_chroot << EOF
sed -i 's+^autologin-user=+#autologin-user=+' /etc/lightdm/lightdm.conf
EOF
