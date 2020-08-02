#!/bin/bash -e

#Disable all the default screens and also the 4 Raspberry images
#Disable test/rainbow screen
log "Changing boot UI options"
echo "disable_splash=1" >> ${ROOTFS_DIR}/boot/config.txt
sed -i 's+console=tty1+console=tty3+g' ${ROOTFS_DIR}/boot/cmdline.txt
sed -i 's+plymouth\.ignore-serial-consoles.*$+plymouth\.ignore-serial-consoles logo\.nologo consoleblank=0 loglevel=3 vt\.global_cursor_default=0+g' ${ROOTFS_DIR}/boot/cmdline.txt

#Copy the boot splash screen service file 
install -m 644 files/splashscreen.service "${ROOTFS_DIR}/etc/systemd/system"

#Copy the initial boot wizard 
install -m 644 files/firstboot.service "${ROOTFS_DIR}/etc/systemd/system"

#Enable the boot splash screen service
on_chroot << EOF
systemctl disable getty@tty3
systemctl enable splashscreen
systemctl enable firstboot
EOF

#Customizing the values for the PiWizard
log "Customizing the wizard"
sed -i 's+Welcome to Raspberry Pi+Welcome to Eklavya OS+g' ${ROOTFS_DIR}/usr/share/piwiz/piwiz.ui
sed -i 's+Welcome to the Raspberry Pi Desktop!+Welcome to the Eklavya OS Desktop!+' ${ROOTFS_DIR}/usr/share/piwiz/piwiz.ui
sed -i 's+<property name="pixbuf">raspberry-pi-logo.png</property>+<property name="pixbuf">eklavya-icon.png</property>+' ${ROOTFS_DIR}/usr/share/piwiz/piwiz.ui
