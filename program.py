#!/usr/bin/env python
import time
import requests
import json
import RPi.GPIO as io

io.setmode(io.BCM)
 
# Constants
pir_pin = 18

lights_off_delay = 2 
lights_on = False
activate_delay = 0.2

bridge_ip = "192.168.1.8"
hue_user = "2f59282530c009273ae837f135627c53"

group = "nursery"
scene_deep_sea = "726af216a-on-0"

# URL Patterns

hue_url_pattern = "http://{0}/api/{1}/{2}"

hue_url_lights = "lights/"
hue_url_groups = "groups/"
hue_url_set_group_state = hue_url_groups + "{0}/action"

# configure input
io.setup(pir_pin, io.IN)

# initialize
t0 = time.time() - lights_off_delay - 1

# procedures
def turnLightsOn():
    print "Turning lights on!"
    #toggleLightOnOff(2, True)
    #setLightColor(2, 10000, 255, 255)
    startScene(group, scene_deep_sea)
    return True

def turnLightsOff():
    print "Turning lights off!"
    #toggleLightOnOff(2, False)
    toggleGroupOnOff(group, False)
    return False

def getLightStatus():
    url = hue_url_pattern.format(bridge_ip, hue_user, "lights/")
    response = requests.get(url)
    print response
    print response.text

def setLightColor(id, h, s, b):
    url = hue_url_pattern.format(bridge_ip, hue_user, "lights/")
    url += "{0}/state".format(id)
    print url
    j = { 'on': True, 'sat':s, 'bri':b, 'hue':h }
    response = requests.put(url, data=json.dumps(j))
    print response
    print response.text


def toggleLightOnOff(id, on_off):
    url = hue_url_pattern.format(bridge_ip, hue_user, hue_url_lights)
    url += "{0}/state".format(id)
    print url
    j = { 'on': on_off }
    response = requests.put(url, data=json.dumps(j))
    print response
    print response.text

def startScene(group, scene):
    url = hue_url_pattern.format(bridge_ip, hue_user, 
        hue_url_set_group_state.format(group))
    print url
    j = { 'on': True, 'scene': scene }
    response = requests.put(url, data=json.dumps(j))
    print response
    print response.text

def toggleGroupOnOff(group, on_off):
    url = hue_url_pattern.format(bridge_ip, hue_user,
        hue_url_set_group_state.format(group))
    print url
    j = { 'on': on_off }
    response = requests.put(url, data=json.dumps(j))
    print response
    print response.text

# main

getLightStatus()

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
