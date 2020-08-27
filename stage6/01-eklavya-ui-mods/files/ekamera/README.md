# EKamera

Forked from https://github.com/jtpaquet/PiCamera-GUI and customized to work out-of-the-box for Eklavya OS

This program provides a graphical interface (GUI) for the [camera module] (https://www.raspberrypi.org/products/camera-module-v2/) of [Raspberry Pi] (https: //www.raspberrypi. org /).
This program is written in the [Python] programming language (https://www.python.org/) using the Tkinter library.

### Features

* Real-time preview
* Preview the photo taken
* Take photo, video and photos in sequence
* Zoom and move inside the image in real time
* Addition of text and present weather on the photo
* Different photo formats supported
* Horizontal and vertical image rotation and flip

### Installing on Python 3

The most important thing is to make sure that your system contains the picamera packages. To do this, enter the following command in the command prompt of your Raspberry Pi


````
$ sudo apt-get update
$ sudo apt-get install python3-picamera
````

If you are having trouble updating your Raspberry Pi, see this detailed [page] (https://picamera.readthedocs.io/en/release-1.10/install3.html) of the [PiCamera] package documentation ( https://picamera.readthedocs.io/en/release-1.10/index.html).

### Manually installing on Raspberry Pi OS (previously known as Raspbian)

The tool is installed by default on Eklavys OS. If you want to install the tool on Raspberry Pi OS (previously known as Raspbian), pkease run the following commands

```
$ git clone https://github.com/sudeephazra/ekamera.git
$ cd ekamera
$ sudo ./install.sh
```

## Authors

* **Jérémy Talbot-Pâquet** - *Initial work* - [Jtpaquet] (https://github.com/jtpaquet)

Also see the list of [contributors] (https://github.com/jtpaquet/PiCamera-GUI/graphs/contributors) to find out who has contributed to this application.

