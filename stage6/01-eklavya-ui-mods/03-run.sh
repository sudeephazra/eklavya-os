#!/bin/bash -e

#Enable the default wallpaper and logo on the login screen
###May be an update alternative will be required here
on_chroot << EOF
sed -i 's+^wallpaper=.*$+wallpaper=/usr/share/rpd-wallpaper/eklavya_default_wallpaper.png+g' /etc/lightdm/pi-greeter.conf
sed -i 's+^default-user-image=.*$+default-user-image=/usr/share/raspberrypi-artwork/eklavya-logo.png+g' /etc/lightdm/pi-greeter.conf

EOF
