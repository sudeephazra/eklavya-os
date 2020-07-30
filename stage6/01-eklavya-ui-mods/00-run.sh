#!/bin/bash -e

#Disable autologin
on_chroot << EOF
sed -i 's+^autologin-user=+#autologin-user=+g' /etc/lightdm/lightdm.conf
EOF
