#!/bin/bash -e

#Add the EKamera application
log "Add the EKamera application"
cp -Rf files/ekamera "${ROOTFS_DIR}/etc/eklavya"
cp -Rf files/ekamera/ekamera.desktop "${ROOTFS_DIR}/usr/share/applications"
