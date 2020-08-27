#!/bin/bash -e

#Create a custom location for eklavya 
on_chroot << EOF
if [ ! -f "/etc/eklavya" ]; then 
	mkdir -p /etc/eklavya
	mkdir -p /etc/eklavya/images
	mkdir -p /etc/eklavya/icons
	mkdir -p /etc/eklavya/scripts
	
	mkdir -p /tmp/eklavya-msteams
	mkdir -p /tmp/eklavya-zoom
fi
EOF

#Copy files to a staging area
log "Copy files to a staging area"
cp -f files/eklavya_default_wallpaper.png "${ROOTFS_DIR}/etc/eklavya/images"
cp -f files/eklavya_default_bootsplash.png "${ROOTFS_DIR}/etc/eklavya/images"
cp -f files/eklavya_login.png "${ROOTFS_DIR}/etc/eklavya/images"
cp -f files/splashscreen.service "${ROOTFS_DIR}/etc/eklavya/scripts"
cp -f files/firstboot.service "${ROOTFS_DIR}/etc/eklavya/scripts"
#install -m 755 files/noclear.conf "${ROOTFS_DIR}/etc/systemd/system/getty@tty1.service.d/noclear.conf files/firstboot.sh "${ROOTFS_DIR}/etc/eklavya/scripts"
cp -f files/eklavya-icons/*.png "${ROOTFS_DIR}/etc/eklavya/icons"

#Copy the wallpaper into the default location
cp -f files/eklavya_default_wallpaper.png "${ROOTFS_DIR}/usr/share/rpd-wallpaper"

#Enable the default wallpaper on both HDMI ports
log "Enable the default wallpaper on both HDMI ports"
###May be an update alternative will be required here
sed -i 's+^wallpaper=.*$+wallpaper=/usr/share/rpd-wallpaper/eklavya_default_wallpaper.png+g' ${ROOTFS_DIR}/etc/xdg/pcmanfm/LXDE-pi/desktop-items-0.conf
sed -i 's+^wallpaper=.*$+wallpaper=/usr/share/rpd-wallpaper/eklavya_default_wallpaper.png+g' ${ROOTFS_DIR}/etc/xdg/pcmanfm/LXDE-pi/desktop-items-1.conf

#Copy the icons
log "Copy the icons"
#This is a large logo (512x512)
cp -f files/eklavya-logo.png "${ROOTFS_DIR}/usr/share/raspberrypi-artwork"

#The following are the icons for each screen size
cp -f files/eklavya-icons/eklavya_16.png "${ROOTFS_DIR}/usr/share/icons/PiXflat/16x16/places/eklavya-icon.png"
cp -f files/eklavya-icons/eklavya_24.png "${ROOTFS_DIR}/usr/share/icons/PiXflat/24x24/places/eklavya-icon.png"
cp -f files/eklavya-icons/eklavya_32.png "${ROOTFS_DIR}/usr/share/icons/PiXflat/32x32/places/eklavya-icon.png"
cp -f files/eklavya-icons/eklavya_48.png "${ROOTFS_DIR}/usr/share/icons/PiXflat/48x48/places/eklavya-icon.png"
cp -f files/eklavya-icons/eklavya_64.png "${ROOTFS_DIR}/usr/share/icons/PiXflat/64x64/places/eklavya-icon.png"
cp -f files/eklavya-icons/eklavya_80.png "${ROOTFS_DIR}/usr/share/icons/PiXflat/80x80/places/eklavya-icon.png"
cp -f files/eklavya-icons/eklavya_96.png "${ROOTFS_DIR}/usr/share/icons/PiXflat/96x96/places/eklavya-icon.png"
cp -f files/eklavya-icons/eklavya_128.png "${ROOTFS_DIR}/usr/share/icons/PiXflat/128x128/places/eklavya-icon.png"

#To enable Eklavya icon as a system icon
cp -f files/eklavya-icons/eklavya_48.png "${ROOTFS_DIR}/usr/share/icons/hicolor/48x48/apps/eklavya-icon.png"
cp -f files/eklavya-icons/eklavya_48.png "${ROOTFS_DIR}/usr/share/raspberrypi-artwork/eklavya-icon.png"

#Copy the updated OS information
log "Copy the updated OS information"
cp -f files/os-release "${ROOTFS_DIR}/usr/lib/os-release"

#Copy the files for MS Teams
log "Copy the files for MS Teams"
cp -f files/msteams/msteams-icon.png "${ROOTFS_DIR}/usr/share/icons/hicolor/48x48/apps/msteams-icon.png"
install -m 755 files/msteams/msteams.desktop "${ROOTFS_DIR}/usr/share/applications/"
install -m 755 files/msteams/msteams.sh "${ROOTFS_DIR}/etc/eklavya/scripts/"

#Copy the files for Zoom
log "Copy the files for Zoom"
cp -f files/zoom/zoom-icon.png "${ROOTFS_DIR}/usr/share/icons/hicolor/48x48/apps/zoom-icon.png"
install -m 755 files/zoom/zoom.desktop "${ROOTFS_DIR}/usr/share/applications/"
install -m 755 files/zoom/zoomconf.sh "${ROOTFS_DIR}/etc/eklavya/scripts/"
