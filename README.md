# pi-hue-motion
Motion Sensing Philips Hue with a Raspberry Pi

A Python interface to your hue lights, to be run on a Raspberry Pi.

I'm using a PIR motion sensor connected to the GPIO port to detect motion in the room.

https://www.adafruit.com/products/189

# Configuring Pi to start script on boot
Setup the script as a Linux daemon service, using technique here:
http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/

# Now with auto-deploy using a webhook!