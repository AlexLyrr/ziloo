# Video

Video4Linux (V4L for short) is a collection of device drivers and an API for supporting realtime video capture on Linux systems. It is used to receive data from two embedded Vision Sensor chips. These sensors are selected to provide 1080p in low light conditions. 
Current options are [OV2732](../../Hardware/datasheets/OmniVision_OV2732.pdf), [OV2740](../../Hardware/datasheets/OmniVision_OV2740.pdf), [OV2718](../../Hardware/datasheets/OmniVision_OV2718.pdf), [GC2053](../../Hardware/datasheets/AE-2M-3043_GC2053_CSP_Datasheet_Release_V11_20181212.pdf) and GC2093.

For more V4L information refer to 
[Rockchip ISP](https://linuxtv.org/downloads/v4l-dvb-apis/admin-guide/rkisp1.html#rockchip-image-signal-processor-rkisp1),
[i.MX Video Capture Driver](https://linuxtv.org/downloads/v4l-dvb-apis/admin-guide/imx.html#i-mx-video-capture-driver),
[I2C sub-device drivers](https://linuxtv.org/downloads/v4l-dvb-apis/driver-api/v4l2-subdev.html#i2c-sub-device-drivers),
[V4L v2 API spec](https://www.linuxtv.org/downloads/legacy/video4linux/API/V4L2_API/spec-single/v4l2.html),
[V4L2 events](https://linuxtv.org/downloads/v4l-dvb-apis/driver-api/v4l2-event.html#v4l2-events),
[Videobuf Framework](https://linuxtv.org/downloads/v4l-dvb-apis/driver-api/v4l2-videobuf.html#videobuf-framework),
[MIPI CSI-2 video ops](https://linuxtv.org/downloads/v4l-dvb-apis/driver-api/csi2.html#mipi-csi-2),
[V4L Utils source code](https://git.linuxtv.org/v4l-utils.git/tree),
[Other doc for Linux TV](https://linuxtv.org/downloads/v4l-dvb-apis/), 
and [Video for Linux resources](http://www.exploits.org/v4l/).

[MPP](https://github.com/rockchip-linux/mpp/tree/develop/doc/design) 
is developed by Rockchip and may be a more performant alternative to V4L.
I must be considered as a foundation based on the demo applications.
Perhaps we just use it to encode video for UVC ouput.

For into on USB video in Linux refer to [OpenWRT USB Video](https://oldwiki.archive.openwrt.org/doc/howto/usb.video), [USB video device class](https://en.wikipedia.org/wiki/USB_video_device_class), and [USB Documentation](https://www.usb.org/documents).


## Capture speed

Video is captured while Ziloo Occi is awake. The rate of capture is adjusted to meet the demands on Subcognition processes. Each process subscribes at a rate of 1fps to 30fps.

It is recommended that processes request 4fps.

## Process recognition step(s)

Processes will receive the 4 most recent frames and the most recently tagged reference frames.

As part of recognition step the processes can,

* Tag a recent frame to be a type of reference frame.
* Define recognised objects in latest frame
* Save a framebuffer derived from the latest frame to be used in subsequent steps 

As part of the less frequent **full frame** recognition step the process can,

* Tag a recent frame to be a type of reference frame.
* Define recognised objects in latest frame
* Save a framebuffer derived from the latest frame to be used in subsequent steps 


## Focus area

Based on known objects recently(1 sec) present the focus within the captured images is defined.
Regular frames are cropped to the focus area.


## Full frames

A full frame is passed between 0.1fps and 1fps to recognisers to allow them to identify anticipatory events.


## RGB vs IR

Under low light conditions the IR camera is used. When lighting is good the RGB camera is used.

Both cameras are only used for stereo vision and face security checks.

## USB Webcam streaming

The platform can function as a webcam when connected to a PC or Raspberry Pi.
It supports USB Video Gadget(UVC) streaming at the current capture speed.


## Recording

The inputs can be recorded to storage on the side.
TODO details of what is recorded.


TODO processes asking for config params. FPS, Blur factor, Color precision, White balance.
