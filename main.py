#!/usr/bin/env python

"""
  Copyright (c) 2019, Isuru Walpola
  StudioW (http://studiow.cf)
  All Rights Reserved

"""
import modbusdevice as modbus
from datetime import datetime, time

"""
initiate deviceCollection dictionary
"""

deviceCollection = {
	"d1" : modbus.Device(a=1,i='127.0.0.1', name = 'd1'),
	"d2" : modbus.Device(a=1,i='127.0.0.1', name = 'd2'),
	"d3" : modbus.Device(a=1,i='127.0.0.1', name = 'd3')
}

""" instantiate persistant storage """
persistance = helpers.Persistance()

""" query and update persistant data """
def refresh_persistance(xx):
	if xx.last_set_time.day<datetime.now().day: #check if valid and update if necessary
		newinitvals=[200,200,200] #replace withfunction to read
		xx.update(initdata=newinitvals)
	#print "finished refreshing"
	#print xx.data

""" query device array """
def query_devices(deviceCollection):
	for device in deviceCollection:
		deviceCollection[device].read()


