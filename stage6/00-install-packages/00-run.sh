#!/bin/bash -e

#Adding repo for VSCode
on_chroot << EOF
wget -qO - https://gitlab.com/paulcarroty/vscodium-deb-rpm-repo/raw/master/pub.gpg | sudo apt-key add -
echo 'deb https://paulcarroty.gitlab.io/vscodium-deb-rpm-repo/debs/ vscodium main' | sudo tee --append /etc/apt/sources.list.d/vscodium.list
EOF

on_chroot << EOF
apt update
apt-get -y dist-upgrade
apt-get clean
EOF

