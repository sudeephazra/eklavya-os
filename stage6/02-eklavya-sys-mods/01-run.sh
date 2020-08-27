#!/bin/bash -e

# Enabling the camera by default
log "Enabling the camera by default"

on_chroot << EOF
./files/enable_camera.sh 1
EOF
