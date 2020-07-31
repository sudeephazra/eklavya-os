#!/bin/bash -e

#Cleanup
on_chroot << EOF
apt autoremove
apt-get clean
apt-get autoremove --purge
EOF

#Update the repository
on_chroot << EOF
apt-get update
EOF
