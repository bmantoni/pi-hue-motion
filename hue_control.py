import random
import requests
import json
import logging

class HueControl(object):

	hue_url_pattern = "http://{0}/api/{1}/{2}"

	hue_url_lights = "lights/"
	hue_url_groups = "groups/"
	hue_url_set_group_state = hue_url_groups + "{0}/action"

	# right now I'm assuming these already exist.
	# TODO - create them
	scenes = {
	 'deep_sea': "726af216a-on-0",
	 'blue_rain': "0f2c67d80-on-0",
	 'sunset': "087f88f52-on-0",
	 'reading': "e915785b2-on-0" }
	
	def __init__(self, bridge_ip, user):
		self.bridge_ip = bridge_ip
		self.user = user
		
	# for now just random, later do something fancier
	def getSceneToUse(self):
		return random.choice(self.scenes.values())

	# url formatting
	def getLightsUrl(self):
		return self.hue_url_pattern.format(self.bridge_ip, self.user, self.hue_url_lights)

	def getLightStatus(self):
		self.logResponse( requests.get(self.getLightsUrl()) )
		
	def setLightColor(self, id, h, s, b):
		url = self.getLightsUrl()
		url += "{0}/state".format(id)
		j = { 'on': True, 'sat':s, 'bri':b, 'hue':h }
		self.doPutRequest(url, j)

	def toggleLightOnOff(self, id, on_off):
		url = self.getLightsUrl() + "{0}/state".format(id)
		j = { 'on': on_off }
		self.doPutRequest(url, j)
		
	def startScene(self, group, scene=None):
		if not scene:
			scene = self.getSceneToUse()
			
		url = self.hue_url_pattern.format(self.bridge_ip, self.user, 
			self.hue_url_set_group_state.format(group))
		logging.debug("Start scene url: " + url)
		j = { 'on': True, 'scene': scene }
		self.doPutRequest(url, j)

	def toggleGroupOnOff(self, group, on_off):
		url = self.hue_url_pattern.format(self.bridge_ip, self.user,
			self.hue_url_set_group_state.format(group))
		j = { 'on': on_off }
		self.doPutRequest(url, j)

	def doPutRequest(self, url, body):
		response = requests.put(url, data=json.dumps(body))
		self.logResponse(response)

	def logResponse(self, r):
		logging.debug(r)
		logging.debug(r.text)
