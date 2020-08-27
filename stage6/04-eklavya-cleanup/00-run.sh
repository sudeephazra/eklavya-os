#!/bin/bash -e

#Cleanup
log "Running cleanup"
on_chroot << EOF
apt autoremove
apt-get clean
apt-get autoremove --purge
EOF

#Update the repository
on_chroot << EOF
apt-get update
EOF
