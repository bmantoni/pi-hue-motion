#!/usr/bin/env python
import time
import random
import requests
import json
import logging
import RPi.GPIO as io

io.setmode(io.BCM)

logging.basicConfig(filename='/home/pi/pi-hue-motion/hue-motion.log', level=logging.INFO)

# Constants
pir_pin = 18

lights_off_delay = 90
lights_on = False
activate_delay = 0.2

bridge_ip = "192.168.1.8"
hue_user = "2f59282530c009273ae837f135627c53"

group = "nursery"
scenes = {
 'deep_sea': "726af216a-on-0",
 'blue_rain': "0f2c67d80-on-0",
 'sunset': "087f88f52-on-0",
 'reading': "e915785b2-on-0" }

# URL Patterns

hue_url_pattern = "http://{0}/api/{1}/{2}"

hue_url_lights = "lights/"
hue_url_groups = "groups/"
hue_url_set_group_state = hue_url_groups + "{0}/action"

# configure input
io.setup(pir_pin, io.IN)

# initialize
t0 = time.time() - lights_off_delay - 1

# for now just random, later do something fancier
def getSceneToUse():
   return random.choice(scenes.values())

# procedures
def turnLightsOn():
    logging.info("Turning lights on!")
    #toggleLightOnOff(2, True)
    #setLightColor(2, 10000, 255, 255)
    #startScene(group, scene_deep_sea)
    startScene(group, getSceneToUse())
    
    return True

def turnLightsOff():
    logging.info("Turning lights off!")
    #toggleLightOnOff(2, False)
    toggleGroupOnOff(group, False)
    return False

def getLightStatus():
    url = hue_url_pattern.format(bridge_ip, hue_user, "lights/")
    response = requests.get(url)
    logging.debug(response)
    logging.debug(response.text)

def setLightColor(id, h, s, b):
    url = hue_url_pattern.format(bridge_ip, hue_user, "lights/")
    url += "{0}/state".format(id)
    j = { 'on': True, 'sat':s, 'bri':b, 'hue':h }
    response = requests.put(url, data=json.dumps(j))
    logging.debug(response)
    logging.debug(response.text)


def toggleLightOnOff(id, on_off):
    url = hue_url_pattern.format(bridge_ip, hue_user, hue_url_lights)
    url += "{0}/state".format(id)
    print url
    j = { 'on': on_off }
    response = requests.put(url, data=json.dumps(j))
    logging.debug(response)
    logging.debug(response.text)

def startScene(group, scene):
    url = hue_url_pattern.format(bridge_ip, hue_user, 
        hue_url_set_group_state.format(group))
    logging.debug("Start scene url: " + url)
    j = { 'on': True, 'scene': scene }
    response = requests.put(url, data=json.dumps(j))
    logging.debug(response)
    logging.debug(response.text)

def toggleGroupOnOff(group, on_off):
    url = hue_url_pattern.format(bridge_ip, hue_user,
        hue_url_set_group_state.format(group))
    print url
    j = { 'on': on_off }
    response = requests.put(url, data=json.dumps(j))
    logging.debug(response)
    logging.debug(response.text)

# main

logging.info(" --- Startup ---")
getLightStatus()
# on startup they'll turn on here then immediately turn off (below)
# just to show the program has started
lights_on = turnLightsOn()

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
