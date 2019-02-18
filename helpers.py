import pickle
from datetime import datetime, time

"""Object for for persistant data"""

class Persistance(object):
	min_time = time(6,0,0) #6 a.m
	def __init__(self):
		self.rawdata = pickle.load(open('storage_data.pkl', 'rb'))
		self.last_set_time = datetime.strptime(self.rawdata[0],"%Y:%m:%d %H:%M:%S")
		self.device_data = self.rawdata[1]

	def update(self, savedata):
		self.last_set_time = datetime.now()
		self.device_data = savedata
		self.rawdata[0] = self.last_set_time.strftime("%Y:%m:%d %H:%M:%S")
		self.rawdata[1] = self.device_data
		pickle.dump(self.data, open('storage_data.pkl', 'wb'), pickle.HIGHEST_PROTOCOL)