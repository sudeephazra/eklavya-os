#!/bin/bash -e

#Enable the default wallpaper and logo on the login screen 
log "Enable the default wallpaper and logo on the login screen"
sed -i 's+^wallpaper=.*$+wallpaper=/etc/eklavya/images/eklavya_login.png+g' ${ROOTFS_DIR}/etc/lightdm/pi-greeter.conf
sed -i 's+^default-user-image=.*$+default-user-image=/usr/share/raspberrypi-artwork/eklavya-logo.png+g' ${ROOTFS_DIR}/etc/lightdm/pi-greeter.conf

#Customize the quick launch bar to have Firefox, File Browser and Deepin Terminal
log "Customize the quick launch bar to have Firefox, File Browser and Deepin Terminal"
sed -i 's+=chromium-browser\.desktop*$+=firefox-esr\.desktop+g' ${ROOTFS_DIR}/etc/xdg/lxpanel/LXDE-pi/panels/panel
sed -i 's+=lxde-x-www-browser\.desktop*$+=firefox-esr\.desktop+g' ${ROOTFS_DIR}/etc/xdg/lxpanel/LXDE-pi/panels/panel
sed -i 's+=lxterminal\.desktop*$+=deepin-terminal\.desktop+g' ${ROOTFS_DIR}/etc/xdg/lxpanel/LXDE-pi/panels/panel

#Customize to have the start menu
log "Customize to have the start menu"
sed -i 's+image=start-here$+image=eklavya-icon+g' ${ROOTFS_DIR}/etc/xdg/lxpanel/LXDE-pi/panels/panel




