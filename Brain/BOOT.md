# Booting Ziloo

The [boot ROM (BROM)](https://linux-sunxi.org/BROM#U-Boot_SPL_limitations) is written in the SoC and cannot be changed. 

After power-up, the A10/A20 boots from an integrated, non-replaceable 32 KiB ROM chip (Boot ROM or BROM). This could be considered the primary program-loader. The SoC starts to fetch instructions from address 0xffff0000 which is where the BROM is located at. The BROM split up into two parts: The first part (at 0xffff0000) is the FEL mode and the second is the eGON.BRM (located at 0xffff4000).


## EGON Flash / SSD boot

The Allwinner A10, A13, A20 and A31 boot as noted over several places, BROM is the first step in booting and is baked into chip itself. Moving from the BROM, Allwinner boots something called boot0 and boot1 from NAND. The magicvalue for the AllWinner bootloader in various places is 'eGON' and thus the bootloader shall be known as such.


### eGON.BRM

The BROM bootloader has been extracted from the chip and can be found in hno's repository.. The magic signature is "eGON.BRM". The BROM seems to start at 0x4000. If the BROM has identified boot0 in NAND loads and executes it.

* [Allwinner V3s BROM](https://github.com/FunKey-Project/Allwinner-V3s-BROM)
* [BROM images](https://github.com/hno/Allwinner-Info/tree/master/BROM)
* Further reading: [Sunxi EGON](https://linux-sunxi.org/EGON#eGON.BRM).


## Fallback / Recovery FEL boot

FEL is a low-level subroutine contained in the BootROM on Allwinner devices. It is used for initial programming and recovery of devices using USB.

Further reading: [FEL](https://linux-sunxi.org/FEL)


## U-Boot loading linux 

The default way to load linux is

BROM -> SPL -> [U-Boot](https://github.com/experientials/u-boot) -> Linux Kernel

1. First stage – Boot ROM
This is the primary program loader residing on a read-only flash memory (ROM) integrated directly into the processor chip.
It contains the very first code which is executed on power-on or reset.
Depending on the configuration of the bootstrap pins or internal fuses it may decide from which media to load and run the next piece of software. In case of a Secure Boot processor it will also verify the code authenticity before its execution.
At this stage, Boot ROM code is not aware about memory type and different interconnected peripherals.
The main goal here is to perform basic peripherals initialization such as PLLs, system clocks setup then find a boot device from which load a bootloader such as u-Boot.

2. Second stage – SPL
A typical u-Boot image is around few hundreds KB size (~300KB) which does not fit inside internal SRAM of most ARM processor. They are typically less than 100KB.
To handle this limitation, u-Boot adopted the SPL (Secondary Program Loader) approach which consists of creating a very small pre-loader that after configuring and initializing peripherals and the main system memory can load the full blown u-Boot.
It shares the same u-Boot’s sources but with a minimal set of code.
So when u-Boot is built for a platform that requires SPL, it generate two binaries : SPL (MLO file) and u-Boot image.

3. Third stage – u-Boot
Das u-Boot aims to offer a flexibel way to load and start the Linux Kernel from a different type of devices, it also provides rich features for a bootloader, such as a command line interface, Shell Scripting, Support of a variety of Filesystems, networking and other options that are very helpful during initial Hardware Bring-Up and development process, but can be bypassed for the production by enabling the Falcon-Mode and save by the way some precious seconds of the boot time !

* [Das U-Boot repository](https://github.com/experientials/u-boot)
* [Arch Linux ARM - U-Boot bootloaders for Allwinner-based boards [32-bit]](https://github.com/RoEdAl/alarm-uboot-sunxi-armv7)
* [Setting Up U-Boot to Harden the Boot Process](https://www.vdoo.com/blog/setting-up-u-boot-to-harden-the-boot-process)


### Fast Boot Linux with u-Boot Falcon Mode


[Falcon mode](https://github.com/experientials/u-boot/blob/master/doc/README.falcon) is 
a feature in u-Boot that enables fast booting by allowing SPL directly to start Linux kernel 
and skip completely u-boot loading and initialization.

[Full Article](https://embexus.com/2017/05/07/fast-boot-linux-with-u-boot-falcon-mode/)


## Maix SD Card format deconstructed

0x2000 -> 0xDFFF (sector 16 - 111) with "eGON" is this SPL?
0x1DE00 -> 0x1E009 (sector 239) with MSWIN 4.1 NO NAME FAT16. Is this a partition marker?
0x2D000 +10 bytes (sector 360) F8FFFFF....
0x3C000 +0x5A (sector 480) with "Info sys volume" is this GPT partition?

Should the u-boot be copied as 0x2000 -> 0xFFFFF

> dd bs=1k count=1016 skip=8 if=v831_dd.img of=u-boot-extract.img


root@e591091e200a:/# fdisk -l /workspace/images/maixpy3-v831-800m-64m-512m-sp2305_240240_20210802_dd.img 
Disk /workspace/images/maixpy3-v831-800m-64m-512m-sp2305_240240_20210802_dd.img: 480 MiB, 503316480 bytes, 983040 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: AB6F3888-569A-4926-9668-80941DCB40BC

Device                                                                       Start    End Sectors  Size Type
/workspace/images/maixpy3-v831-800m-64m-512m-sp2305_240240_20210802_dd.img1  49152  49663     512  256K Microsoft basic data
/workspace/images/maixpy3-v831-800m-64m-512m-sp2305_240240_20210802_dd.img2  49664  61951   12288    6M Microsoft basic data
/workspace/images/maixpy3-v831-800m-64m-512m-sp2305_240240_20210802_dd.img3  61952 717311  655360  320M Microsoft basic data
/workspace/images/maixpy3-v831-800m-64m-512m-sp2305_240240_20210802_dd.img4 717312 881151  163840   80M Microsoft basic data
/workspace/images/maixpy3-v831-800m-64m-512m-sp2305_240240_20210802_dd.img5 881152 983006  101855 49.8M Microsoft basic data
root@e591091e200a:/# parted -l /workspace/images/maixpy3-v831-800m-64m-512m-sp2305_240240_20210802_dd.img 
Model: Virtio Block Device (virtblk)
Disk /dev/vda: 68.7GB
Sector size (logical/physical): 512B/4096B
Partition Table: msdos
Disk Flags: 

Number  Start   End     Size    Type     File system  Flags
 1      1049kB  68.7GB  68.7GB  primary  ext4         boot


Partition 1: 25'165'824 (49152) 0x1800000
Partition 2: 25'427'968 (29664) 0x1840000

```
/scripts/extract-card.sh /workspace/images/maixpy3-v831-800m-64m-512m-sp2305_240240_20210802_dd.img
```

```output
Model:  (file)
Disk /workspace/images/maixpy3-v831-800m-64m-512m-sp2305_240240_20210802_dd.img: 503316480B
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags: 

Number  Start       End         Size        File system     Name    Flags
 1      25165824B   25427967B   262144B                     env     msftdata
 2      25427968B   31719423B   6291456B                    boot    msftdata
 3      31719424B   367263743B  335544320B  ext4            rootfs  msftdata
 4      367263744B  451149823B  83886080B   linux-swap(v1)  swap    msftdata
 5      451149824B  503299583B  52149760B   fat32           UDISK   msftdata

Disk /workspace/images/maixpy3-v831-800m-64m-512m-sp2305_240240_20210802_dd.img: 480 MiB, 503316480 bytes, 983040 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: AB6F3888-569A-4926-9668-80941DCB40BC

Device                                                                       Start    End Sectors  Size Type
/workspace/images/maixpy3-v831-800m-64m-512m-sp2305_240240_20210802_dd.img1  49152  49663     512  256K Microsoft 
/workspace/images/maixpy3-v831-800m-64m-512m-sp2305_240240_20210802_dd.img2  49664  61951   12288    6M Microsoft 
/workspace/images/maixpy3-v831-800m-64m-512m-sp2305_240240_20210802_dd.img3  61952 717311  655360  320M Microsoft 
/workspace/images/maixpy3-v831-800m-64m-512m-sp2305_240240_20210802_dd.img4 717312 881151  163840   80M Microsoft 
/workspace/images/maixpy3-v831-800m-64m-512m-sp2305_240240_20210802_dd.img5 881152 983006  101855 49.8M Microsoft 
```



## Other References


* [Sunxi Buildroot](https://linux-sunxi.org/Buildroot)
* [Allwinner Boot / FEL / FES / NAND Dump](https://xor.co.za/post/2018-12-01-fel-bootprocess/)

Partition magics: τφα1  1Ξ 2Ξ 3Ξ 

