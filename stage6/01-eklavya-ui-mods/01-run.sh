#!/bin/bash -e

#Create a custom location for eklavya 
on_chroot << EOF
if [ ! -f "/etc/eklavya" ]; then 
	mkdir -p /etc/eklavya
	mkdir -p /etc/eklavya/images
	mkdir -p /etc/eklavya/icons
	mkdir -p /etc/eklavya/scripts
fi
EOF

#Copy files to a staging area
cp -f files/eklavya_default_wallpaper.png "${ROOTFS_DIR}/etc/eklavya/images"
cp -f files/eklavya_default_bootsplash.png "${ROOTFS_DIR}/etc/eklavya/images"
cp -f files/splashscreen.service "${ROOTFS_DIR}/etc/eklavya/scripts"
cp -f files/firstboot.service "${ROOTFS_DIR}/etc/eklavya/scripts"
cp -f files/firstboot.sh "${ROOTFS_DIR}/etc/eklavya/scripts"
cp -f files/eklavya-icons/*.png "${ROOTFS_DIR}/etc/eklavya/icons"

#Copy the wallpaper into the default location
cp -f files/eklavya_default_wallpaper.png "${ROOTFS_DIR}/usr/share/rpd-wallpaper"

#Enable the default wallpaper on both HDMI ports
###May be an update alternative will be required here
sed -i 's+^wallpaper=.*$+wallpaper=/usr/share/rpd-wallpaper/eklavya_default_wallpaper.png+g' ${ROOTFS_DIR}/etc/xdg/pcmanfm/LXDE-pi/desktop-items-0.conf
sed -i 's+^wallpaper=.*$+wallpaper=/usr/share/rpd-wallpaper/eklavya_default_wallpaper.png+g' ${ROOTFS_DIR}/etc/xdg/pcmanfm/LXDE-pi/desktop-items-1.conf

#Copy the icons
#This is a large logo (512x512)
cp -f files/eklavya-logo.png "${ROOTFS_DIR}/usr/share/raspberrypi-artwork"

#The following are the icons for each screen size
cp -f files/eklavya-icons/eklavya_16.png "${ROOTFS_DIR}/usr/share/icons/PiXflat/16x16/places/eklavya-icon.png"
cp -f files/eklavya-icons/eklavya_24.png "${ROOTFS_DIR}/usr/share/icons/PiXflat/24x24/places/eklavya-icon.png"
cp -f files/eklavya-icons/eklavya_32.png "${ROOTFS_DIR}/usr/share/icons/PiXflat/32x32/places/eklavya-icon.png"
cp -f files/eklavya-icons/eklavya_48.png "${ROOTFS_DIR}/usr/share/icons/PiXflat/48x48/places/eklavya-icon.png"

#To enable Eklavya icon as a system icon
cp -f files/eklavya-icons/eklavya_48.png "${ROOTFS_DIR}/usr/share/icons/hicolor/48x48/apps/eklavya-icon.png"
cp -f files/eklavya-icons/eklavya_48.png "${ROOTFS_DIR}/usr/share/raspberrypi-artwork/eklavya-icon.png"

#To enable the icon for Eklavya Wizard
cp -f files/eklavya-icons/eklavya_56.png "${ROOTFS_DIR}/usr/share/piwiz/eklavya-icon.png"

#Copy the updated OS information
cp -f files/os-release "${ROOTFS_DIR}/usr/lib/os-release"

