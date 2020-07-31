#!/bin/bash -e

#Create a custom location for eklavya 
on_chroot << EOF
if [ ! -f "/etc/eklavya" ]; then 
	mkdir -p /etc/eklavya
	mkdir -p /etc/eklavya/images
	mkdir -p /etc/eklavya/scripts
fi
EOF

#Copy files to a staging area
cp -f files/eklavya_default_wallpaper.png "${ROOTFS_DIR}/etc/eklavya/images"
cp -f files/eklavya_default_bootsplash.png "${ROOTFS_DIR}/etc/eklavya/images"
cp -f files/splashscreen.service "${ROOTFS_DIR}/etc/eklavya/scripts"

#Copy the wallpaper into the default location
cp -f files/eklavya_default_wallpaper.png "${ROOTFS_DIR}/usr/share/rpd-wallpaper"

#Enable the default wallpaper on both HDMI ports
###May be an update alternative will be required here
on_chroot << EOF
sed -i 's+^wallpaper=.*$+wallpaper=/usr/share/rpd-wallpaper/eklavya_default_wallpaper.png+g' /etc/xdg/pcmanfm/LXDE-pi/desktop-items-0.conf
sed -i 's+^wallpaper=.*$+wallpaper=/usr/share/rpd-wallpaper/eklavya_default_wallpaper.png+g' /etc/xdg/pcmanfm/LXDE-pi/desktop-items-1.conf

EOF

#Copy the icons
cp -f files/eklavya-logo.png "${ROOTFS_DIR}/usr/share/raspberrypi-artwork"

#Copy the wallpaper into the default location
cp -f files/os-release "${ROOTFS_DIR}/usr/lib/os-release"

#Update the repository
on_chroot << EOF
apt-get update
EOF
