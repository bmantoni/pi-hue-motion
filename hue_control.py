import time
import random
import requests
import json
import logging

# what to do, and when to do it
class LightAction(object):
    def __init__(self, when, action):
        self.when = when
        self.action = action

class Effects(object):

    # Assuming these exist. Created manually with Hue app.
    scenes = {
        'deep_sea': "a91b0640b-on-0",
        'blue_rain': "4f3190be7-on-0" }

    actions = {
        'bedtime': LightAction(
            lambda p: p >= 17 and p < 22,
            lambda g, self: self.setOneLightInGroup(g, 1, 962, 252, 151) ),
        'middleOfTheNight': LightAction(
            lambda p: p >= 22 or p < 6,
            lambda g, self: self.startScene(g, Effects.scenes['deep_sea']) ),
        'morning': LightAction(
            lambda p: p >= 6 and p < 10,
            lambda g, self: self.startScene(g, Effects.scenes['blue_rain']) ),
        'daytime': LightAction(
            lambda p: p >= 10 and p < 17,
            lambda g, self: self.startColorLoop(g) )
        }
    
class HueControl(object):

    hue_url_pattern = "http://{0}/api/{1}/{2}"

    hue_url_lights = "lights/"
    hue_url_get_light = hue_url_lights + "{0}/"
    hue_url_set_light_state = hue_url_get_light + "state"
    hue_url_groups = "groups/"
    hue_url_get_group = hue_url_groups + "{0}/"
    hue_url_set_group_state = hue_url_get_group + "action"
    
    def __init__(self, bridge_ip, user):
        self.bridge_ip = bridge_ip
        self.user = user

    def doTimeBasedAction(self, group):
        r = [name for name in Effects.actions if Effects.actions[name].when( time.localtime().tm_hour )]
        a = None
        if len(r) < 1:
            # current hour doesn't have an action defined, pick randomly
            a = random.choice(Effects.actions.keys())
        if not a:
            # get the first or only element
            a = r[0]
            
        logging.debug("Selected action based on time of day: " + a)
        Effects.actions[a].action(group, self)

    # url formatting
    def getLightsUrl(self):
        return self.hue_url_pattern.format(self.bridge_ip, self.user, self.hue_url_lights)

    def getLightStatus(self):
        self.logResponse( requests.get(self.getLightsUrl()) )
        
    # sets one light to a color and sets the others in the group off
    def setOneLightInGroup(self, group, id, h, s, b):
        url = self.hue_url_pattern.format(self.bridge_ip, self.user,
            self.hue_url_get_group.format(group))
        
        groupAttrs = requests.get(url)
        print groupAttrs.text
        print groupAttrs.json["lights"]
        
        for l in filter(lambda p: p != str(id), groupAttrs.json["lights"]):
            logging.debug("turning off light " + l)
            self.toggleLightOnOff(l, False)
            
        logging.debug("turning on light " + str(id))
        self.setLightColor(id, h, s, b)
        
    def setLightColor(self, id, h, s, b):
        url = self.getLightsUrl()
        url += "{0}/state".format(id)
        j = { 'on': True, 'sat':s, 'bri':b, 'hue':h, "colormode": "hs" }
        self.doPutRequest(url, j)

    def toggleLightOnOff(self, id, on_off):
        url = self.getLightsUrl() + "{0}/state".format(id)
        j = { 'on': on_off }
        self.doPutRequest(url, j)
        
    def doGroupAction(self, group):
        self.doTimeBasedAction(group)
        
    def startScene(self, group, scene):            
        url = self.hue_url_pattern.format(self.bridge_ip, self.user, 
            self.hue_url_set_group_state.format(group))
        logging.debug("Start scene url: " + url)
        j = { 'on': True, 'scene': scene }
        self.doPutRequest(url, j)
        
    def startColorLoop(self, group):            
        url = self.hue_url_pattern.format(self.bridge_ip, self.user, 
            self.hue_url_set_group_state.format(group))
        logging.debug("Start scene url: " + url)
        j = { 'on': True, 'effect': 'colorloop' }
        self.doPutRequest(url, j)

    def toggleLightOnOff(self, light, on_off):
        url = self.hue_url_pattern.format(self.bridge_ip, self.user,
            self.hue_url_set_light_state.format(light))
        j = { 'on': on_off }
        self.doPutRequest(url, j)
        
    def toggleGroupOnOff(self, group, on_off):
        url = self.hue_url_pattern.format(self.bridge_ip, self.user,
            self.hue_url_set_group_state.format(group))
        j = { 'on': on_off }
        self.doPutRequest(url, j)
        
    # def createGroup(self, lights, name):
        # TODO
        # {"lights": ["1", "2", "3"], "name": "nursery"}

    def doPutRequest(self, url, body):
        response = requests.put(url, data=json.dumps(body))
        self.logResponse(response)

    def logResponse(self, r):
        logging.debug(r)
        logging.debug(r.text)
