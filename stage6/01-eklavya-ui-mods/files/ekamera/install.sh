#!/bin/bash

#Script to install the tool on Raspberry Pi 4 running Eklavys OS 
if [ "$(id -u)" != "0" ]; then
	echo "Please run as root" 1>&2
	exit 1
fi
if [ -f "/etc/eklavya/ekamera" ]; then 
	rm -Rf /etc/eklavya/ekamera
    mkdir -p /etc/eklavya/ekamera
fi

cp -Rf * /etc/eklavya/ekamera
cp -Rf ekamera.desktop /usr/share/applications/