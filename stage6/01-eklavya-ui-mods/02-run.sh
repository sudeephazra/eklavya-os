#!/bin/bash -e

#Disable all the default screens and also the 4 Raspberry images
echo " disable_splash=1 " >> "${ROOTFS_DIR}/boot/config.txt"
#Disable test/rainbow screen
echo " logo.nologo consoleblank=0 loglevel=1 quiet " >> "${ROOTFS_DIR}/boot/cmdline.txt"

#Copy the boot splash screen service file 
install -m 644 files/splashscreen.service "${ROOTFS_DIR}/etc/systemd/system"

#Enable the boot splash screen service
on_chroot << EOF
systemctl disable getty@tty3
systemctl enable splashscreen
EOF

