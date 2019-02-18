#!/usr/bin/env python

"""
  Copyright (c) 2019, Isuru Walpola
  StudioW (http://studiow.cf)
  All Rights Reserved

"""
import modbusdevice as modbus
from datetime import datetime
from datetime import time as dtime
import pyglet
import time

"""
initiate deviceCollection dictionary
"""
"""Should fake? put 0 for no, 1 for yes"""
fake = 0

deviceCollection = {
	"d1" : modbus.Device(a=1,i='127.0.0.1', name = 'd1', fake = fake),
	"d2" : modbus.Device(a=1,i='127.0.0.1', name = 'd2', fake = fake),
	"d3" : modbus.Device(a=1,i='127.0.0.1', name = 'd3', fake = fake)
}
sumDailyDelta = 0
sumMonthlyDelta = 0

"""set program start and end time"""
prog_start = dtime(6,0,0)
prog_end = dtime(18,0,0)

""" query device array """
def query_devices(deviceCollection):
	for device in deviceCollection:
		if not deviceCollection[device].online_status
			deviceCollection[device].connect()
		if deviceCollection[device].online_status
			deviceCollection[device].read()
			deviceCollection[device].calcdelta()
		if deviceCollection[device].online_status:
			sumDailyDelta += deviceCollection[device].daily_delta
			sumMonthlyDelta += deviceCollection[device].monthly_delta

def update_display():
	print "currently empty"

"""main script"""
"""Run once"""
#Setup the window
#window = pyglet.window.Window()
#image = pyglet.resource.image('kitten.png')
#def on_draw():
#    window.clear()
#    image.blit(0, 0)
#pyglet.app.run()

"""Scheduling loop every 10 minutes"""
starttime=time.time()
while True:
	time_now = datetime.now().time()
	if time_now>prog_start and time_now<prog_end
		query_devices(deviceCollection)
		update_display()
	time.sleep(600.0 - ((time.time() - starttime) % 600.0))
