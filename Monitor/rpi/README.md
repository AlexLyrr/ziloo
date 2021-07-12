# Raspberry Pi Setup

Boot on Rapberry Pi on a Raspbian SD Card. Run `sudo apt install gparted`.

To create an SSD or USB drive write Raspbian OS as an image. Leave the boot partition alone. 
Moving `rootfs` isn't supported. Expand rootfs size to 7536MB. Add an extended partition for the rest.

After booting on the SSD/USB. Open a terminal in `/home/pi`.

```bash
git clone https://github.com/experientials/ziloo-firmware
cd ziloo-firmware
./setup/rpi-develop
```




```
sudo apt install gparted less nano gdb-multiarch qemu-user-static wget curl
sudo apt install cmake gcc-arm-linux-gnueabi g++-arm-linux-gnueabi crossbuild-essential-armel crossbuild-essential-armhf
```

