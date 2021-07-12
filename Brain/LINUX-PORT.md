# Linux Port of Allwinner V831

[Sipeed MAIX-II](https://www.seeedstudio.com/Sipeed-MAIX-Dock-p-4815.html) is a camera focused ARM SoC 
based on Allwinner V831. It has a firmware with U-Boot and OpenWRT based Tina Linux that boots and runs correctly.

The aim is to create an equivalent [port](https://gitlab.alpinelinux.org/alpine/aports/-/tree/master/) for [Alpine Linux](https://alpinelinux.org).

You must deliver,

- A working SD Card image that can boot Maix-II with Alpine Linux
- A docker build image to run the build of the pieces
- A build that will produce U-Boot
- A build that will produce Linux kernel
- A build that will produce the core packages



## Alpine Port

Alpine builds a [Generic ARM distro](https://alpinelinux.org/downloads/). A port specific to V831 is needed.
A variant similar to the Tina Linux port for V831 is [Tina Linux for R329](https://github.com/sipeed/R329-Tina-jishu).
Notice that R329 has apparently recently been mainlined in the Linux repository.

[postmarketOS](https://postmarketos.org) is based on Alpine Linux. It is built to be a fully open source base to port
to mobile phones. A main target is the PIN64 PinePhone which is based on Allwinner A64. This could be used as the 
basis for making a port for V831.

PostmarketOS (Alpine) links,

* [Porting to a new device](https://wiki.postmarketos.org/wiki/Porting_to_a_new_device)
* [Ported devices](https://wiki.postmarketos.org/wiki/Devices)
* [DIY Fully working Alpine Linux for Allwinner and Other ARM SOCs](https://wiki.alpinelinux.org/wiki/DIY_Fully_working_Alpine_Linux_for_Allwinner_and_Other_ARM_SOCs)
* [Alpine on ARM](https://wiki.alpinelinux.org/wiki/Alpine_on_ARM)
* 

Other related builds,

* [Build script for NanoPi NEO Alpine Linux image](https://github.com/dragonflylee/nanopi-alpine) and [NanoPi on SUNXI](https://linux-sunxi.org/FriendlyARM_NanoPi_NEO_%26_AIR)
* [Lindenis V833](http://wiki.lindeni.org/index.php/Lindenis_V833)
* [Tina Linux for R329](https://github.com/sipeed/R329-Tina-jishu)
* [2 year old Allwinner buildroot](https://gitee.com/MicroScale/allwinner-buildroot)
* [3 year old FriendlyARM H3 Linux port](https://github.com/friendlyarm/h3_lichee)



## U-Boot Port

U-Boot must be extended with support for booting on V831
It seems that support for V831 has already been added to [Xboot](https://github.com/xboot/xboot).
Otherwise it should be possible to acquire the u-boot port via Sochip or Lidenis.



## Filesystems

For this port the kernel and overlays can be saved with a FAT partition as it's normally done with Alpine Linux.
The Linux Kernel should support:

- FAT
- extFS 4
- squashfs
- F2FS
- JFFS2

[Alpine filesystems wiki](https://wiki.alpinelinux.org/wiki/Filesystems)


## Expected Packages

It should be possible to install packages that don't come out of the box with `apk` tool.

For reference there is [a list of packages in the default image](./MAIX-II-PACKAGES.md)

Related,

* [R329 Tina Linux Packages](https://github.com/sipeed/r329-package).


## Hardware Device Drivers

Minimum hardware support

- USB 2.0 OTG connector
- SD Card

Fully porting [the Maix-II hardware](https://dl.sipeed.com/shareURL/MaixII/maix-ii%20datasheet_v1.02_en-US.pdf) is seen as a second part to be achieved after booting.
There must however be a plan to the following

- Microphone In
- Audio Out
- SP2305 FHD Camera
- A.I. Subsystem NPU
- Wifi via RTL8189FTV
- 1.3" 240px x 240px LCD
- Ethernet 100 Mbps


Other features forseen:

- Booting via USB
- Keyboard/Mouse connection via USB-OTG
- Exposing SD Card contents v



## Delivery

- A working SD Card image that can boot Maix-II
- A docker build image to run the build
- A build that will produce U-Boot
- A build that will produce Linux kernel
- A build that will produce the core packages


Push a brach to [Experientials GitHub](https://github.com/experientials/ziloo-firmware) with the build scripts and instructions needed.
Push a brach to [Experientials GitHub](https://github.com/experientials/aport) with the linux port (and uboot?).
Full SD Card image with documentation of how it is structured and a script to construct the image