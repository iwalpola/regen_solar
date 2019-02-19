#!/usr/bin/env python

"""
  Copyright (c) 2019, Isuru Walpola
  StudioW (http://studiow.cf)
  All Rights Reserved

"""
import sys
import modbusdevice as modbus
from datetime import datetime, time
if sys.version_info[0] >= 3:
	import PySimpleGUI as sg
else:
	import PySimpleGUI27 as sg

"""Test variables"""
uofr = 0 #Should update on first retrievl?, put 1 for yes
fake = 1 #Should fake? put 0 for no, 1 for yes

"""Set updation frequency in seconds"""
update_interval = 60

"""set program start and end time"""
prog_start = time(9,18,0)
prog_end = time(21,0,0)

"""
initiate deviceCollection dictionary
"""

deviceCollection = {
	"d1" : modbus.Device(a=1,i='127.0.0.1', name = 'd1', fake = fake, uofr = uofr),
	"d2" : modbus.Device(a=1,i='127.0.0.1', name = 'd2', fake = fake, uofr = uofr),
	"d3" : modbus.Device(a=1,i='127.0.0.1', name = 'd3', fake = fake, uofr = uofr)
}

sumkW = 0
sumDailyDelta = 0
sumMonthlyDelta = 0
sumkWh = 0

""" query device array """
def query_devices():
	for device in deviceCollection:
		if not deviceCollection[device].online_status:
			deviceCollection[device].connect()
			print "reconnection attempted"
		if deviceCollection[device].online_status:
			deviceCollection[device].read()
			deviceCollection[device].update_persistance()
			deviceCollection[device].calcdelta()
			global sumDailyDelta
			global sumMonthlyDelta
			global sumkW
			global sumkWh
			sumkW = 0
			sumkWh = 0
			sumDailyDelta = 0
			sumMonthlyDelta = 0
			sumDailyDelta += deviceCollection[device].daily_delta
			sumMonthlyDelta += deviceCollection[device].monthly_delta
			sumkW += deviceCollection[device].kW
			sumkWh += deviceCollection[device].kWh

def update_display():
	# print "display curently undefined"
	# print "Current Generation (kW): " + str(sumkW)
	# print "Total Monthly Energy (kWh): " + str(sumMonthlyDelta)
	# print "Total Daily Energy (kWh): " + str(sumDailyDelta)
	print "update display"
	window.FindElement('_ckW_').Update(str(sumkW))
	window.FindElement('_dkWh_').Update(str(sumDailyDelta))
	window.FindElement('_mkWh_').Update(str(sumMonthlyDelta))
	window.FindElement('_ltkWh_').Update(str(sumkWh))

layout = [[sg.Text('Latest Data')],
		[sg.Text('Current Generation (kW):',size=(22,1),font=('Helvetica', 20)), sg.Text('', key='_ckW_',size=(8,1),font=('Helvetica', 20))],
		[sg.Text('Total Daily Energy (kWh):',size=(22,1),font=('Helvetica', 20)), sg.Text('', key='_dkWh_',size=(8,1),font=('Helvetica', 20))],
		[sg.Text('Total Monthly Energy (kWh):',size=(22,1),font=('Helvetica', 20)), sg.Text('', key='_mkWh_',size=(8,1),font=('Helvetica', 20))],
		[sg.Text('Lifetime Energy (kWh):',size=(22,2),font=('Helvetica', 20)), sg.Text('', key='_ltkWh_',size=(8,2),font=('Helvetica', 20))],
		[sg.Button('Restart'), sg.Button('Exit')]]

window = sg.Window('Ananda College Solar Monitor').Layout(layout)
"""Run once"""
event, values = window.Read(timeout=1)
print "entered main sequence"
query_devices()
update_display()
"""Scheduling loop every n seconds"""
while True:
	time_now = datetime.now().time()
	event, values = window.Read(timeout=update_interval*1000)
	if event == 'Exit':
		break
	elif time_now>prog_start and time_now<prog_end:
		query_devices()
		update_display()
	else: print "doing nothing"
window.Close()