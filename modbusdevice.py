import sunspec.core.client as client
import json
from datetime import datetime
import time
import random

""" Device class represents and manipulates Sunspec Devices on the network. """

class Device(object):

	def __init__(self, a=1, i='', name='device_friendly_name', fake=0):
		self.a = a
		self.fake = fake
		self.i = i
		self.P = 502
		self.T = 2.0
		self.name = name
		self.kW = 0
		self.kWh = 0
		self.daily_delta = 0
		self.monthly_delta = 0
		self.persistance = {"monthly_initial" : {"last_set": datetime.now(), "value": 0}, "daily_initial": {"last_set": datetime.now(), "value": 0}}
		self.connect()
		self.read()
		self.retrieve()
		self.calcdelta()

	def connect(self):
		if self.fake:
			self.online_status = 1
		else:
			""" Create a new inverter device """
			self.online_status = 0
			try:
				self.connection = client.SunSpecClientDevice(client.TCP, self.a, ipaddr=self.i, ipport=self.P, timeout=self.T)
				self.online_status = 1
			except client.SunSpecClientError, e:
				print 'Error: %s' % (e)
				self.online_status = 0

	def read(self):
		if self.fake:
			self.kW = random.randint(200, 3200)
			self.kWh = (int(time.time()/100000)+random.randint(100, 500))
		elif self.online_status:
			try:
				self.connection.inverter.read()
				self.kW = (self.connection.inverter.points[14])/1000
				self.kWh = (self.connection.inverter.points[24])/1000
			except e:
				self.online_status = 0

	def calcdelta(self):
		if self.online_status:
			self.monthly_delta = self.kWh - self.persistance["monthly_initial"]["value"]
			self.daily_delta = self.kWh - self.persistance["daily_initial"]["value"]
	
	def retrieve(self):
		f = open(self.name+'.data','r')
		self.persistance = json.load(f)
		f.close()
		self.persistance["daily_initial"]["last_set"] = datetime.strptime(self.persistance["daily_initial"]["last_set"],"%Y:%m:%d %H:%M:%S")
		self.persistance["monthly_initial"]["last_set"] = datetime.strptime(self.persistance["monthly_initial"]["last_set"],"%Y:%m:%d %H:%M:%S")
		#call read() to update vlues before potential persistance
		#check if init values expired, and update
		if self.persistance["daily_initial"]["last_set"].date<datetime.today().date:
			print "daily initial updated for "+self.name
			self.persist(daily=1)
		if self.persistance["monthly_initial"]["last_set"].replace(day=1).date<datetime.now().replace(day=1).date:
			print "monthly initial updated for "+self.name
			self.persist(monthly=1)

	def persist(self, daily = 0, monthly = 0):
		if self.kWh==0 and self.online_status:
			print "zero kWh value not allowed to persist"
			return
		now = datetime.now()
		if daily:
			self.persistance["daily_initial"]["value"] = self.kWh
			self.persistance["daily_initial"]["last_set"] = now

		if monthly:
			self.persistance["monthly_initial"]["value"] = self.kWh
			self.persistance["monthly_initial"]["last_set"] = now
		
		self.persistance["daily_initial"]["last_set"] = self.persistance["daily_initial"]["last_set"].strftime("%Y:%m:%d %H:%M:%S")
		self.persistance["monthly_initial"]["last_set"] = self.persistance["monthly_initial"]["last_set"].strftime("%Y:%m:%d %H:%M:%S")
		
		f = open(self.name+'.data','w+')
		json.dump(self.persistance,f)
		f.close()
		self.persistance["daily_initial"]["last_set"] = datetime.strptime(self.persistance["daily_initial"]["last_set"],"%Y:%m:%d %H:%M:%S")
		self.persistance["monthly_initial"]["last_set"] = datetime.strptime(self.persistance["monthly_initial"]["last_set"],"%Y:%m:%d %H:%M:%S")