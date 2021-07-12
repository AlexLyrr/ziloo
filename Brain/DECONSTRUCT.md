# Reverse engineer Tina Linux Buildroot config

An SD Card image was built for a development board by Sipeed. In order to construct a compatible
SD Card with a different structure I need to deconstruct how the image is built.
The existing firmware is a build of Tina Linux which is a derivative of OpenWRT dedicated to video hardware.


[Disk Image(v831_sipedd_210606_dd.img.gz)](https://dl.sipeed.com/shareURL/MaixII/SDK/release).

As deliverables I need a working build script to recreate an SD Card that will boot the 
developer board. It doesn't have to recreate all of the packages, but it must construct a working
boot system and Linux core equivalent to OpenWRT.

Parts of the build:

- Buildroot for U-Boot
- Buildroot for Linux
- Documentation of how images for SPL, U-Boot and Linux are tied together on SD Card
- Dockerfile

The version of U-Boot and Linux can be based on the same versions or newer than what is on the image.

Ideally this build can work by only relying on open source such as [Sunxi tools](http://linux-sunxi.org/Sunxi-tools). If needed this can rely on Allwinner SDK for the Chipset (V831/V833), in which case the download and install must be documented.

As part of the build configuration a Dockerfile must be provided that can run the full build process
which constructed a full image and individual partition images.

If possible document how various newer Allwinner SoC boot from SD Card such as V833.

If possible document how the Rockchip RV1126 boots from SD Card.

Related information

- [Sunxi BROM](https://linux-sunxi.org/BROM)
- [FEL USB Boot](http://linux-sunxi.org/FEL)
- [FunKey with V3s](https://github.com/FunKey-Project/Allwinner-V3s-BROM)
