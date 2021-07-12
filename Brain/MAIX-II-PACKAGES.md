# Packages

The starting point is to support the Maix-II packages coming from an OpenWRT codebase in the form of Tina Linux.
Tina Linux is somewhat hard to track down as it is mostly Chinese and hosted behind developer account logins.

Some locations with Tina Linux,

* [Lindenix V536 packages](https://gitee.com/lindenis/lindenis-v536-package)
* [Lindenis V833 Lichee Brandy 2.0 U-Boot 2018](https://gitee.com/lindenis/lindenis-v833-lichee-brandy-2.0-u-boot-2018)
* [Lindenis V833 Lichee Linux 4.9](https://gitee.com/lindenis/lindenis-v833-lichee-linux-4.9)
* [Lindenis V833 softwinner](https://gitee.com/lindenis/lindenis-v833-softwinner)
* [Lindenis V833 Tina Target](https://gitee.com/lindenis/lindenis-v833-target)
* [Tina Linux V2 Version SDK build](https://gitee.com/lindenis/lindenis-v833-build)
* [Lindenis Allwinner V5 MPP Sample code](https://gitee.com/lindenis/mpp_sample)
* [Tina Linux V2 SDK docs](https://gitee.com/lindenis/lindenis-v833-docs)
* [Tina Linux quick start guide](https://gitee.com/lindenis/lindenis-v833-docs/blob/master/Tina%20Linux%20quick%20start%20guide.md)


## Core packages

The core packages in Tina Linux.

```
busybox - 1.27.2-3 - The Swiss Army Knife of embedded Linux.
busybox-init-base-files - 167-1612350358
busybox-init-base-files - 167-1612257817 - This package contains a busybox init base filesystem and system scripts f.
ca-certificates - 20160104 - System CA certificates
dropbear - 2015.71-2 - A small SSH2 server/client designed for small memory environments.
e2fsprogs - 1.42.12-1 - This package contains essential ext2 filesystem utilities which consists of
libext2fs - 1.42.12-1 - libext2fs is a library which can access ext2, ext3 and ext4 filesystems.
libffi - 3.0.13-1 - The libffi library provides a portable, high level programming interface to
libc - -1
libgcc - -1 - GCC support library
libgdbm - 1.11-1 - GNU database manager library
libpthread - -1 - POSIX thread library
librt - -1 - POSIX.1b RealTime extension library
libuapi - 1-1 - unit api for allwinner
zlib - 1.2.8-1 - zlib is a lossless data-compression library.
```

The expected Alpine packages.

- busybox 1.33.1-r4
- ca-certificates 20191127-r5
- dropbear 2020.81-r0
- e2fsprogs	1.46.2-r0
- f2fs-tools 1.14.0-r0
- libffi 3.3-r2
- zlib 1.2.11-r3



## Kernel modules

Installed in Tina Linux. These seem to be provided through overlays not related to packages.

```
kernel - 4.9.118-1-c166dfd81804ce13f1769d26dc1448a4
kmod-8189fs - 4.9.118-1 - 8189fs support (staging)
kmod-cfg80211 - 4.9.118-1 - Kernel modules for CFG80211 support
kmod-spi-dev - 4.9.118-1 - This package contains the user mode SPI device driver
kmod-vin-v4l2 - 4.9.118-1 - Video input support (staging)
```


## Multimedia and device packages

The multimedia packages in Tina Linux.

```
alsa-lib - 1.1.4.1-1 - This is the library package for alsa, needed by some userspace programs.
alsa-utils - 1.1.0-1 - ALSA (Advanced Linux Sound Architecture) utilities
eyesee-mpp-external - 1.0-1 - eyesee-mpp-external contains some external libs which are needed by other mpp modules.
eyesee-mpp-middleware - 1.0-1 - eyesee-mpp-middleware contain eyesee-mpp basic libraries.
eyesee-mpp-system - 1.0-1 - eyesee-mpp-system is as eyesee-mpp low level libraries.
libAWIspApi - 1-1 - camera VIN ISP api for allwinner
libjpeg - 9a-1 - The Independent JPEG Group's JPEG runtime library
libcairo - 1.14.6-1 - Cairo is a 2D graphics library with support for multiple output devices.
libpixman - 0.34.0-1 - Pixman is a low-level software library for pixel manipulation
libpng - 1.2.56-1 - A PNG format files handling library
libwebp - 0.4.3-1 - webp libraries
opencv - 4.1.0 - OpenCV (Open Source Computer Vision Library) is an open source computer vision and machine learning.
tinyalsa-lib - 1.1.1-34ffa583936aeb6938636c9c0a26a322b69b0d26 - TinyALSA is a small library to interface with ALSA i.
tinyalsa-utils - 1.1.1-34ffa583936aeb6938636c9c0a26a322b69b0d26 - This package contains utilities provided by TinyAL.
```

The expected Alpine packages.

- alsa-lib 1.2.5-r2	
- alsa-utils 1.2.5-r2
- libjpeg 9d-r1
- libpng 1.6.37-r1
- libwebp 1.2.0-r2
- opencv 4.5.2-r0



### Eyesee MPP

It seems that this is a package specific to Allwinner SoC.

The [Lindenis SDK](https://github.com/lindenis-org/lindenis-v833-softwinner) seems to contain object/library [files covering this](https://github.com/lindenis-org/lindenis-v833-softwinner/tree/master/eyesee-mpp).

If possible this should be added to the firmware.


### Maix Legacy packages

There doesn't seem to be any need for MicroPython at this time. The packages relate to Maix-I.

* micropython - 1.9.4-2 - This package contains Micro Python, a lean and fast implementation of the Python 3.4 programe
* micropython-lib - 1.9.3-1 - This package contains micropython-lib, a project to develop a non-monolothic


## Maix 3 API packages

MaixPy3 is based on Linux where MaixPy was based on MicroPython.

* MaixPy3 - [0.2.5-1](https://github.com/sipeed/MaixPy3/tree/MaixPy3-0.2.5) - a cross-platform package with c & py.
* libmaix - [0.0.1-1](https://github.com/sipeed/libmaix/tree/v0.1.0) - maix middleware libs
* camerademo - 1.0-1 - camerademo test sensor
* sipeed_memtool - 0.0.1-1 - Sipeed tools memtool
* sipeed_update_dtb - 0.0.1-1 - Sipeed tools update_dtb


## Networking

curl - 7.54.1-1 - A client-side URL transfer utility
hostapd-common - 2017-11-08-2 - hostapd/wpa_supplicant common support files
iperf3 - 3.0.11-1 - Iperf is a modern alternative for measuring TCP and UDP bandwidth
libcurl - 7.54.1-1 - A client-side URL transfer library
libnghttp2 - 1.24.0 - tools in nghttp2, eg: nghttp nghttpd nghttpx h2load
libopenssl - 1.1.0i-1 - The OpenSSL Project is a collaborative effort to develop a robust,
libuclient - 2016-01-28-2e0918c7e0612449024caaaa8d44fb2d7a33f5f3 - HTTP/1.1 client library
wget - 1.20.1-3 - Wget is a network utility to retrieve files from the Web using http
wpa-cli - 2017-11-08-2 - WPA Supplicant command line interface
wpa-supplicant - 2017-11-08-2 - WPA Supplicant

The expected Alpine packages.

- curl 7.78.0-r0
- iperf3 3.10.1-r0
- libcurl 7.78.0-r0	
- wget 1.21.1-r1


## Python packages

python-pip-conf - 0.1-1 - Configuration file for pip/pip3
python3 - 3.8.5-2 - This package contains the (almost) full Python install.
python3-asyncio - 3.8.5-2 - Python 3.8 asyncio module
python3-base - 3.8.5-2 - This package contains only the interpreter and the bare minimum
python3-certifi - 2020.6.20-1 - Certifi is a carefully curated collection of Root Certificates for validating the
python3-cgi - 3.8.5-2 - Python 3.8 cgi module
python3-cgitb - 3.8.5-2 - Python 3.8 cgitb module
python3-chardet - 3.0.4-4 - Universal encoding detector for Python 2 and 3
python3-codecs - 3.8.5-2 - Python 3.8 codecs + unicode support
python3-ctypes - 3.8.5-2 - Python 3.8 ctypes module
python3-dbm - 3.8.5-2 - Python 3.8 dbm module
python3-decimal - 3.8.5-2 - Python 3.8 decimal module
python3-distutils - 3.8.5-2 - Python 3.8 distutils module
python3-email - 3.8.5-2 - Python 3.8 email module
python3-evdev - 1.4.0-2 - Bindings to the Linux input handling subsystem
python3-gdbm - 3.8.5-2 - Python 3.8 gdbm module
python3-gpiod - 1.4.0-2 - A fast and complete Python implementation of gpiod.
python3-idna - 2.10-1 - A library to support the Internationalised Domain Names in Applications
python3-light - 3.8.5-2 - This package is essentially the python3-base package plus
python3-logging - 3.8.5-2 - Python 3.8 logging module
python3-lzma - 3.8.5-2 - Python 3.8 lzma module
python3-multiprocessing - 3.8.5-2 - Python 3.8 multiprocessing
python3-ncurses - 3.8.5-2 - Python 3.8 ncurses module
python3-numpy - 1.19.2-1 - NumPy is the fundamental package for array computing with Python.
python3-openssl - 3.8.5-2 - Python 3.8 SSL module
python3-pillow - 7.2.0-1 - The friendly PIL fork
python3-pip - 20.1.1-1 - Python 3.8 pip module
python3-pkg-resources - 47.1.0-1 - Python 3.8 pkg_resources module (part of setuptools)
python3-plumbum - 1.6.9-2 - A fast and complete Python implementation of plumbum.
python3-pyasn1 - 0.4.8-2 - This is an implementation of ASN.1 types and codecs in Python programming
python3-pydoc - 3.8.5-2 - Python 3.8 pydoc module
python3-pyserial - 3.4-2 - This module encapsulates the access for the serial port. It provides backends
python3-qrcode - 6.1-3 - Pure python QR Code generator
python3-requests - 2.24.0-1 - Requests is the only Non-GMO HTTP library for Python, safe for human consumption
python3-rpyc - 5.0.1-3 - rpyc
python3-rsa - 4.6-1 - Is a pure-Python RSA implementation. It supports encryption and decryption,
python3-schedule - 0.6.0-2 - An in-process scheduler for periodic jobs that uses the builder pattern for configurati.
python3-setuptools - 47.1.0-1 - Python 3.8 setuptools module
python3-six - 1.15.0-1 - Six is a Python 2 and 3 compatibility library.  It provides utility functions
python3-spidev - 3.5-2 - Bindings to the Linux input handling subsystem
python3-sqlite3 - 3.8.5-2 - Python 3.8 sqlite3 module
python3-unittest - 3.8.5-2 - Python 3.8 unittest module
python3-urllib - 3.8.5-2 - Python 3.8 URL library module
python3-urllib3 - 1.25.10-1 - HTTP library with thread-safe connection pooling, file post, and more.
python3-xml - 3.8.5-2 - Python 3.8 xml libs



## Debugging / Development packages

harfbuzz - 1.7.4-1 - HarfBuzz is an OpenType text shaping engine.
fontconfig - 2.12.1-3 - The Fontconfig package contains a library and support programs used for
libfreetype - 2.5.5-2 - The FreeType project is a team of volunteers who develop free,
libncurses - 5.9-3 - Terminal handling library
libncursesw - 5.9-3 - Terminal handling library (Unicode)
mtd - 21 - This package contains an utility useful to upgrade from other firmware or
terminfo - 5.9-3 - Terminal Info Database (ncurses)
spidev-test - 4.9.118-4.9.118 - SPI testing utility.


## OpenWRT modules

jsonfilter - 2014-06-19-cdc760c58077f44fc40adbbe41e1556a67c1b9a9 - OpenWrt JSON filter utility
libubus - 2016-01-26-619f3a160de4f417226b69039538882787b3811c - OpenWrt RPC client library
logd - 2016-03-07-fd4bb41ee7ab136d25609c2a917beea5d52b723b - OpenWrt system log implementation
netifd - 2016-02-01-3610a24b218974bdf2d2f709a8af9e4a990c47bd - OpenWrt Network Interface Configuration Daemon
ubox - 2016-03-07-fd4bb41ee7ab136d25609c2a917beea5d52b723b - OpenWrt system helper toolbox
ubus - 2016-01-26-619f3a160de4f417226b69039538882787b3811c - OpenWrt RPC client utility
ubusd - 2016-01-26-619f3a160de4f417226b69039538882787b3811c - OpenWrt RPC daemon
opkg - 9c97d5ecd795709c8584e972bfdf3aee3a5b846d-10 - Lightweight package management system
uclient-fetch - 2016-01-28-2e0918c7e0612449024caaaa8d44fb2d7a33f5f3 - Tiny wget replacement using libuclient



## Other packages

```
fbviewer - 1 - Frame buffer viewer image
glib2 - 2.50.1-1 - The GLib library of C routines
glog - 0.3.5-2 - This repository contains a C++ implementation of the Google logging
icu - 55.1-1 - International Components for Unicode
jshn - 2016-02-26-5326ce1046425154ab715387949728cfb09f4083 - Library for parsing and generating JSON from shell scris
libattr - 20150922-1 - Extended attributes support
libblobmsg-json - 2016-02-26-5326ce1046425154ab715387949728cfb09f4083 - blobmsg <-> json conversion library
libbz2 - 1.0.6-2 - bzip2 is a freely available, patent free, high-quality
libdb47 - 4.7.25.4.NC-5 - Berkeley DB library (4.7).
libexpat - 2.1.0-3 - A fast, non-validating, stream-oriented XML parsing library.
libjson-c - 0.12-1 - This package contains a library for javascript object notation backends.
libjson-script - 2016-02-26-5326ce1046425154ab715387949728cfb09f4083 - Minimalistic JSON based scripting engine
liblua - 5.1.5-1 - Lua is a powerful light-weight programming language designed for extending
liblzma - 5.2.2-1 - liblzma library from XZ Utils
libnl-tiny - 0.1-5 - This package contains a stripped down version of libnl
libpcre - 8.38-2 - A Perl Compatible Regular Expression library
libreadline - 6.3-1 - The Readline library provides a set of functions for use by applications
libsqlite3 - 3120200-1 - SQLite is a small C library that implements a self-contained, embeddable,
libstdcpp - -1 - GNU Standard C++ Library v3
libubox - 2016-02-26-5326ce1046425154ab715387949728cfb09f4083 - Basic utility library
libuci - 2016-02-02.1-1 - C library for the Unified Configuration Interface (UCI)
libuuid - 2.25.2-4 - The UUID library is used to generate unique identifiers for objects
libxml2 - 2.9.3-1 - A library for manipulating XML and HTML resources.
lrzsz - 0.12.20-2 - Transfer files in your login sessions.
rwcheck - 1-1 - rwcheck to check read and write by CRC, just data correctness but not performance.
uci - 2016-02-02.1-1 - Utility for the Unified Configuration Interface (UCI)
```
