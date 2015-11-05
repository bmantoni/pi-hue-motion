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
  filename='hue-motion.log', # /home/pi/pi-hue-motion/hue-motion.log
  format='%(asctime)s %(message)s',
  level=logging.INFO)


# Constants
pir_pin = 18

lights_off_delay = 90
lights_on = False
activate_delay = 0.2

hue = hue_control.HueControl(
	bridge_ip="192.168.1.8", 
	user="34f30a5a1bdaa117196a4dc63f76c33")

# Assumes this has been created manually. With API.
group = "nursery"

def turnLightsOn():
    logging.info("Turning lights on!")
    hue.doGroupAction(group)
    
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
time.sleep(0.5)

if not on_pi:
	# for testing
	hue.setLightColor(1, 962, 252, 151)
	time.sleep(1.0)
	hue.toggleGroupOnOff(group, False)
	exit(0)

while True:
    if io.input(pir_pin):
        #reset the timer
        t0 = time.time()

    if ( ( time.time() - t0 > lights_off_delay ) and lights_on):
        lights_on = turnLightsOff()
    elif ( ( time.time() - t0 <= lights_off_delay ) and not lights_on):
        lights_on = turnLightsOn()

    time.sleep(activate_delay)
