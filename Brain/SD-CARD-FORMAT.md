# Ziloo SD Card Format

The partitioning scheme is meant to support a range of devices. It is compatible with Raspberry Pi and Embedded ARM devices.
It enables booting on Raspberry Pi to reconfigure it for a specific Embedded ARM development or production device.
It is aimed at embedded devices with a focus on ARM and RISC-V.

Due to the range of devices it is essential to dynamically support different devices.
Raspberry Pi is used to build and test firmware, so the basic format is compatible with RPi4.

The block/sector size is 512 byte. MBR table.

0. 4.2Mb Free Space
1. FAT32 "boot" partition used by Raspberry Pi (400Mb )
<!-- 2. Gap in partition table for U-Boot x12. (12Mb) -->
3. jffs2 "rootfs-a" 750Mb JFFS2 starting point and extensions log for Allwinner/Rockchip/ARM devices
4. jffs2 "rootfs-b" 750Mb JFFS starting point and extensions log for K510/RISC-V devices
5. jffs2 "rootfs-c" spare embedded root FS (750Mb)
6. Swap partition for linux boots (397Mb)
7. RPi extFS 4 "rootfs" (5000Mb) or "data" if no RPi support

Relevant guides,

* [SUNXI Bootable SD card](https://linux-sunxi.org/Bootable_SD_card)



## "boot" partition

This contains files used by Raspberry Pi for booting.

In the boot partition SPL is placed in a "spool" file that is at the beginning at the partition.
In the partition the U-Boot is placed after the spool file in another file called "boot-1", "boot-2" and "boot-3" (or otherwise beginning with boot-). These files contain a device specific U-Boot implementation.


## The Gap

There is a gap to write U-Boot for multiple devices. 
It isn't marked as partition, but is rather a gap between two partitions.


## "rootfs" or "data" partition

This contains a Desktop Linux and/or Data


## Raspbian Packages

Install:

- gparted


## Mounting the SD Card

Good advice on this [superuser thread: Choice of filesystem for GNU/Linux on an SD card](https://superuser.com/questions/248078/choice-of-filesystem-for-gnu-linux-on-an-sd-card#248092).


## Relevant Filesystems

* [Squashfs 4.0 Filesystem](https://www.kernel.org/doc/html/latest/filesystems/squashfs.html)
* [Ceph Distributed File System](https://www.kernel.org/doc/html/latest/filesystems/ceph.html)
* [WHAT IS Flash-Friendly File System (F2FS)?](https://www.kernel.org/doc/html/latest/filesystems/f2fs.html)
* [UBI File System](https://www.kernel.org/doc/html/latest/filesystems/ubifs.html)
* [SquashFS + JFFS2](https://gist.github.com/rikka0w0/f56977f81d1228fc503b00ad7b526aa7)

