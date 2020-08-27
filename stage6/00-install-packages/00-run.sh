#!/bin/bash -e

#Adding repo for VSCode
log "Adding repo for VSCode"
install -m 644 files/vscodium.list "${ROOTFS_DIR}/etc/apt/sources.list.d/"
on_chroot apt-key add - < files/vscodium.gpg.key

on_chroot << EOF
apt-get update
EOF

