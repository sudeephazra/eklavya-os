#!/bin/bash -e

#Disable all the default screens and also the 4 Raspberry images
#Disable test/rainbow screen
log "Changing boot UI options"
echo "disable_splash=1" >> ${ROOTFS_DIR}/boot/config.txt
sed -i 's+console=tty1+console=tty3+g' ${ROOTFS_DIR}/boot/cmdline.txt
sed -i 's+plymouth\.ignore-serial-consoles.*$+plymouth\.ignore-serial-consoles logo\.nologo consoleblank=0 loglevel=3 vt\.global_cursor_default=0+g' ${ROOTFS_DIR}/boot/cmdline.txt

#Copy the boot splash screen service file 
install -m 644 files/splashscreen.service "${ROOTFS_DIR}/etc/systemd/system"

#Enable the boot splash screen service
on_chroot << EOF
systemctl disable getty@tty3
systemctl enable splashscreen
EOF


#Customizing the values for the PiWizard
log "Customizing the first-boot wizard"

#To enable the icon for Eklavya Wizard
cp -f files/eklavya-icons/eklavya_56.png "${ROOTFS_DIR}/usr/share/piwiz/eklavya-icon.png"
cp -f files/eklavya-menu.png "${ROOTFS_DIR}/usr/share/piwiz/"

#Customizing the menu bar and the panel icon
sed -i 's+Welcome to Raspberry Pi+Welcome to Eklavya OS Desktop+g' ${ROOTFS_DIR}/usr/share/piwiz/piwiz.ui
sed -i 's+<property name="icon">/usr/share/raspberrypi-artwork/raspitr\.png</property>+<property name="icon">eklavya-icon.png</property>+' ${ROOTFS_DIR}/usr/share/piwiz/piwiz.ui
#Customizing the main panel of the application
sed -i 's+Welcome to the Raspberry Pi Desktop!+Welcome to the Eklavya Desktop!+' ${ROOTFS_DIR}/usr/share/piwiz/piwiz.ui
sed -i 's+<property name="pixbuf">raspberry-pi-logo.png</property>+<property name="pixbuf">eklavya-icon.png</property>+' ${ROOTFS_DIR}/usr/share/piwiz/piwiz.ui
sed -i 's+Your Raspberry Pi is now set up and ready to go+Your Eklavya Desktop is now set up and ready to go+' ${ROOTFS_DIR}/usr/share/piwiz/piwiz.ui
sed -i 's+restart your Pi so+restart your Eklavya Desktop so+' ${ROOTFS_DIR}/usr/share/piwiz/piwiz.ui
sed -i 's+click the raspberry icon in the top left corner+click the Eklavya icon in the top left corner+' ${ROOTFS_DIR}/usr/share/piwiz/piwiz.ui
sed -i 's+The change will take effect when the Pi is restarted+The change will take effect when Eklavya OS Desktop is restarted+' ${ROOTFS_DIR}/usr/share/piwiz/piwiz.ui
sed -i 's+corner\.png+eklavya-menu\.png+' ${ROOTFS_DIR}/usr/share/piwiz/piwiz.ui

#Check if autostart of the wizard is enabled
if [ -f ${ROOTFS_DIR}/etc/xdg/autostart/piwiz.desktop ]; then
	echo "Autostart enabled for the Wizard"
else
	echo "Autostart not enabled for the Wizard"
fi

#Classification of Electronics Software
echo "Customizing Electronics software to point to the correct menu"
sed -i 's+^Categories=.*$+Categories=Electronics;+' ${ROOTFS_DIR}/usr/share/applications/caneda.desktop
sed -i 's+^Categories=.*$+Categories=Electronics;+' ${ROOTFS_DIR}/usr/share/applications/arduino.desktop
sed -i 's+^Categories=.*$+Categories=Electronics;+' ${ROOTFS_DIR}/usr/share/applications/fritzing.desktop
sed -i 's+^Categories=.*$+Categories=Electronics;+' ${ROOTFS_DIR}/usr/share/applications/smartsim.desktop
