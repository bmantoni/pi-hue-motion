#!/usr/bin/env python
import time
import requests
import json
import RPi.GPIO as io

io.setmode(io.BCM)

# Constants
pir_pin = 18

lights_off_delay = 10
lights_on = False
activate_delay = 0.5

bridge_ip = "192.168.1.8"
hue_user = "2f59282530c009273ae837f135627c53"

hue_url_pattern = "http://{0}/api/{1}/{2}"

hue_json_on = """{{"on":{0}}}"""
hue_json_color = """{{"on":true, "hue":{0}, "sat":{1}, "bri":{2}}}"""

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

def getLightStatus():
    url = hue_url_pattern.format(bridge_ip, hue_user, "lights/")
    response = requests.get(url)
    print response
    print response.text

def turnLightOn(id, h, s, b):
    print "TODO"

def turnLightOff(id):
    url = hue_url_pattern.format(bridge_ip, hue_user, "lights/")
    url += "{0}/state".format(id)
    print url
    j = { 'on': False }
    response = requests.put(url, data=json.dumps(j))
    print response
    print response.text

# main

getLightStatus()
turnLightOff(2)

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
