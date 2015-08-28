#!/usr/bin/env python

# if not working on a pi set to F, for dev/test
on_pi = True
pir_pin = 18

import time
import logging
import hue_control
if on_pi:
	import RPi.GPIO as io
	io.setmode(io.BCM)
	io.setup(pir_pin, io.IN)

logging.basicConfig(
  filename='hue-motion.log', 
  format='%(asctime)s %(message)s',
  level=logging.INFO)


# Constants
pir_pin = 18

lights_off_delay = 90
lights_on = False
activate_delay = 0.2

hue = hue_control.HueControl(
	bridge_ip="192.168.1.8", 
	user="2f59282530c009273ae837f135627c53")

group = "nursery"

def turnLightsOn():
    logging.info("Turning lights on!")
    #toggleLightOnOff(2, True)
    #setLightColor(2, 10000, 255, 255)
    #startScene(group, scene_deep_sea)
    hue.startScene(group)
    
    return True

def turnLightsOff():
    logging.info("Turning lights off!")
    #toggleLightOnOff(2, False)
    hue.toggleGroupOnOff(group, False)
    return False

# MAIN

t0 = time.time() - lights_off_delay - 1
logging.info(" --- Startup ---")
hue.getLightStatus()
# on startup they'll turn on here then immediately turn off (below)
# just to show the program has started
lights_on = turnLightsOn()

while True:
    if on_pi and io.input(pir_pin):
        #reset the timer
        t0 = time.time()

    if ( ( time.time() - t0 > lights_off_delay ) and lights_on):
        lights_on = turnLightsOff()
    elif ( ( time.time() - t0 <= lights_off_delay ) and not lights_on):
        lights_on = turnLightsOn()

    time.sleep(activate_delay)
