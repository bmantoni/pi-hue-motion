#!/usr/bin/env python
import time
import RPi.GPIO as io
io.setmode(io.BCM)

# Constants
pir_pin = 18

lights_off_delay = 10
lights_on = False
activate_delay = 0.5

# configure input
io.setup(pir_pin, io.IN)

# initialize
t0 = time.time() - lights_off_delay - 1

# procedures
def turnLightsOn():
    print "Turning lights on!"
    return True

def turnLightsOff():
    print "Turning lights off!"
    return False

# main

while True:
    if io.input(pir_pin):
        #reset the timer
        t0 = time.time()
        #print("PIR ALARM!")

    if ( ( time.time() - t0 > lights_off_delay ) and lights_on):
        lights_on = turnLightsOff()
    elif ( ( time.time() - t0 <= lights_off_delay ) and not lights_on):
        lights_on = turnLightsOn()

    time.sleep(activate_delay)
