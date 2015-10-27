# pi-hue-motion
Motion Sensing Philips Hue with a Raspberry Pi

A Python interface to your hue lights, to be run on a Raspberry Pi.

Extensible for triggering events and what happens on those events.

In my case, I trigger based on time-of-day, and launch different scenes and/or colors on particular lights.

# Configuring Pi to start script on boot
Setup the script as a Linux daemon service, using technique here:
http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/

