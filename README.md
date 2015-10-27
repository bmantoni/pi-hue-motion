# pi-hue-motion
Motion Sensing Philips Hue with a Raspberry Pi

A Python interface to your hue lights, to be run on a Raspberry Pi.

Extensible for triggering events and what happens on those events.

In my case, I trigger based on time-of-day, and launch different scenes and/or colors on particular lights.

# Getting Started
Follow instructions here to get an API user ID from your bridge:
http://www.developers.meethue.com/documentation/getting-started

Once you have that, update the code with it.

# Hardware
I'm using a PIR motion sensor connected to the GPIO port to detect motion in the room.

https://www.adafruit.com/products/189

# Configuring for your usage
The main loop checks for motion and records the last time motion was detected.
When motion is detected, it turns on the lights.
Once a certain interval without motion has been detected, it turns off the lights.

The action it takes to 'turn on the lights' should be configured. I'm activating a group with one of a number of scenes.

TODO create the scenes, don't assume they're already stored in the bulbs.

# Configuring Pi to start script on boot
Setup the script as a Linux daemon service, using technique here:
http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/

