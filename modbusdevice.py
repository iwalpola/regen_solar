import sunspec.core.client as client
import json
from datetime import datetime, time

""" Device class represents and manipulates Sunspec Devices on the network. """

class Device(object):

	def __init__(self, a=1, i='', name='device_friendly_name'):
		self.a = a
		self.i = i
		self.P = 502
		self.T = 2.0
		self.name = name
		self.kW = 0
		self.kWh = 0
		self.persistance = {"monthly_initial" : {"last_set": datetime.now(), "value": 0}, "daily_initial": {"last_set": datetime.now(), "value": 0}}

	def connect():
		""" Create a new inverter device """
		self.online_status = 0
		try:
			self.connection = client.SunSpecClientDevice(client.TCP, self.a, ipaddr=self.i, ipport=self.P, timeout=self.T)
			self.online_status = 1
		except client.SunSpecClientError, e:
			print 'Error: %s' % (e)
			self.online_status = 0

	def read(self):
		if self.online_status:
			"""
			try:
				self.connection.inverter.read()
				self.kW = self.connection.inverter
				self.kWh = self.connection.inverter
			except e:
				self.online_status = 0
			"""
		else:
			#try connecting again

	def retrieve(self):
		f = open(self.name+'.data','r')
		self.persistance = json.load(f)
		f.close()
		self.persistance["daily_initial"]["last_set"] = datetime.strptime(self.persistance["daily_initial"]["last_set"],"%Y:%m:%d %H:%M:%S")
		self.persistance["monthly_initial"]["last_set"] = datetime.strptime(self.persistance["monthly_initial"]["last_set"],"%Y:%m:%d %H:%M:%S")
		#call read() to update vlues before potential persistance
		#check if init values expired, and update
		if self.persistance["daily_initial"]["last_set"].date<datetime.today().date:
			self.persist(daily=1)
		if self.persistance["monthly_initial"]["last_set"].replace(day=1).date<datetime.now().replace(day=1).date:
			self.persist(monthly=1)

	def persist(self, daily = 0, monthly = 0):
		if self.kWh ==0:
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