#!/bin/bash -e

on_chroot << EOF
apt-get update
apt-get clean
EOF
#apt-get -y dist-upgrade
