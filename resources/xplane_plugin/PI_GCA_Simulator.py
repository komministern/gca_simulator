"""
"""

from XPLMDefs import *
from XPLMGraphics import *
from XPLMProcessing import *
from XPLMDataAccess import *
from XPLMUtilities import *

import socket, time

class PythonInterface:
	def XPluginStart(self):
		global gOutputFile, gPlaneLat, gPlaneLon, gPlaneEl
		self.Name = "GCA Simulation"
		self.Sig =  "Oscar Franzen"
		self.Desc = "A plugin that provides position and time data to a GCA Simulator."

		# File stuff for the recording funcionality
		self.rwy_1_path = XPLMGetSystemPath() + 'rwy1.txt'
		self.rwy_2_path = XPLMGetSystemPath() + 'rwy2.txt'
		self.rwy_1_file = None
		self.rwy_2_file = None


		""" Find the data refs we want to record."""
		self.plane_local_x = XPLMFindDataRef("sim/flightmodel/position/local_x")
		self.plane_local_y = XPLMFindDataRef("sim/flightmodel/position/local_y")
		self.plane_local_z = XPLMFindDataRef("sim/flightmodel/position/local_z")

		"""
		Register our callback for once a second.  Positive intervals
		are in seconds, negative are the negative of sim frames.  Zero
		registers but does not schedule a callback for time.
		"""
		
		self.FlightLoopCB = self.FlightLoopCallback
		XPLMRegisterFlightLoopCallback(self, self.FlightLoopCB, 0.1, 0)
		
		self.ip_address = ''

                #self.UDP_IP = '192.168.1.67'
		self.UDP_ANYIP = ''
		self.UDP_SEND_PORT = 5006
		self.UDP_LISTEN_PORT = 5005

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind((self.UDP_ANYIP, self.UDP_LISTEN_PORT))
		self.sock.settimeout(0.0)

		self.airport_world_coords = []
		self.active_runway = None
		
		self.record = False
		
		return self.Name, self.Sig, self.Desc

	def XPluginStop(self):
		# Unregister the callback
		XPLMUnregisterFlightLoopCallback(self, self.FlightLoopCB, 0)

		if self.rwy_1_file != None:
			self.rwy_1_file.close()
			self.rwy_2_file.close()
			self.rwy_1_file = None
			self.rwy_2_file = None
		
		self.sock.close()

	def XPluginEnable(self):
		return 1

	def XPluginDisable(self):
		pass

	def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
		pass

	def FlightLoopCallback(self, elapsedMe, elapsedSim, counter, refcon):
		# The actual callback.  First we read the sim's time and the data.
		#elapsed = XPLMGetElapsedTime()

		try:
			data, (self.ip_address, _) = self.sock.recvfrom(1024)
		except socket.timeout, e:
			err = e.args[0]
			print err
		except socket.error, e:
			#print e    # This happens everytime on OSX. Error 35. EAGAIN on Mac.
			pass
		else:
			if data:

				if data == 'query':
					print 'sending answer'
					self.sock.sendto('answer', (self.ip_address, self.UDP_SEND_PORT))
					return 0.1

				data_strings = data.split(',')
				
				if data_strings[0] == 'record':
					# The demo airport must be a two runway airport with interworking thr and eor depending on runway.
					self.active_runway = int(data_strings[1])
					self.record = True
					
					print 'record'

					# Open files if not already open
					if self.rwy_1_file == None and self.rwy_2_file == None:
						self.rwy_1_file = open(self.rwy_1_path, 'w')
						self.rwy_2_file = open(self.rwy_2_path, 'w')
					
					self.airport_world_coords = map(float, data_strings[2:])
				else:
					# Close file if file pointers not equal to None
					if self.rwy_1_file != None and self.rwy_2_file != None:
						self.rwy_1_file.close()
						self.rwy_2_file.close()
						self.rwy_1_file = None
						self.rwy_2_file = None
					
					# Reset attributes to None just for good measure (unnecessary really)
					if self.active_runway != None:
						self.active_runway = None
					
					self.airport_world_coords = map(float, data_strings)

				# Get local coords for the plane
				plane_x = XPLMGetDataf(self.plane_local_x)
				plane_y = XPLMGetDataf(self.plane_local_y)
				plane_z = XPLMGetDataf(self.plane_local_z)

				# The exact time at which the plane was in this position
				time_stamp = time.time()

				thr_x, thr_y, thr_z = XPLMWorldToLocal(self.airport_world_coords[0], self.airport_world_coords[1], self.airport_world_coords[2])
				eor_x, eor_y, eor_z = XPLMWorldToLocal(self.airport_world_coords[3], self.airport_world_coords[4], self.airport_world_coords[5])

				# Now, we define the X-vector as the vector between thr and eor, but with the same altitude at both coords (namely the thr altitude)
				temp_eor_x, temp_eor_y, temp_eor_z = XPLMWorldToLocal(self.airport_world_coords[3], self.airport_world_coords[4], self.airport_world_coords[2])
				orthogonal_X_vector_x = temp_eor_x - thr_x
				orthogonal_X_vector_y = temp_eor_y - thr_y
				orthogonal_X_vector_z = temp_eor_z - thr_z

				# We define the Z-vector as the vector between thr and thr, but with an altitude 100m greater.
				temp_thr_x, temp_thr_y, temp_thr_z = XPLMWorldToLocal(self.airport_world_coords[0], self.airport_world_coords[1], self.airport_world_coords[2] + 100.0)
				orthogonal_Z_vector_x = temp_thr_x - thr_x
				orthogonal_Z_vector_y = temp_thr_y - thr_y
				orthogonal_Z_vector_z = temp_thr_z - thr_z

				# Now lets construct the string to be sent
				string_plane = ','.join(map(str, (plane_x, plane_y, plane_z)))
				string_time = str(time_stamp)
				string_airport_local_coords = ','.join(map(str, (thr_x, thr_y, thr_z, eor_x, eor_y, eor_z)))
				string_span_vectors = ','.join(map(str, (orthogonal_X_vector_x, orthogonal_X_vector_y, orthogonal_X_vector_z, orthogonal_Z_vector_x, orthogonal_Z_vector_y, orthogonal_Z_vector_z)))
				string_to_send = ','.join([string_plane, string_time, string_airport_local_coords, string_span_vectors])

				self.sock.sendto(string_to_send, (self.ip_address, self.UDP_SEND_PORT))
				
				if self.record:
				
					# Save the string_to_send to the active runway file
					if self.active_runway == 0:
						self.rwy_1_file.write(string_to_send + '\n')
					elif self.active_runway == 1:
						self.rwy_2_file.write(string_to_send + '\n')
					else:
						print 'ERROR! This should not happen!'

					# Reverse direction and recount points and vectors from the other runways view
					temp_x, temp_y, temp_z = thr_x, thr_y, thr_z
					thr_x, thr_y, thr_z = eor_x, eor_y, eor_z
					eor_x, eor_y, eor_z = temp_x, temp_y, temp_z

					# Now, we define the X-vector as the vector between thr and eor, but with the same altitude at both coords (namely the thr altitude)
					temp_eor_x, temp_eor_y, temp_eor_z = XPLMWorldToLocal(self.airport_world_coords[0], self.airport_world_coords[1], self.airport_world_coords[5])
					orthogonal_X_vector_x = temp_eor_x - thr_x
					orthogonal_X_vector_y = temp_eor_y - thr_y
					orthogonal_X_vector_z = temp_eor_z - thr_z

					# We define the Z-vector as the vector between thr and thr, but with an altitude 100m greater.
					temp_thr_x, temp_thr_y, temp_thr_z = XPLMWorldToLocal(self.airport_world_coords[3], self.airport_world_coords[4], self.airport_world_coords[5] + 100.0)
					orthogonal_Z_vector_x = temp_thr_x - thr_x
					orthogonal_Z_vector_y = temp_thr_y - thr_y
					orthogonal_Z_vector_z = temp_thr_z - thr_z

					# Now lets construct the string to be sent
					string_plane = ','.join(map(str, (plane_x, plane_y, plane_z)))
					string_time = str(time_stamp)
					string_airport_local_coords = ','.join(map(str, (thr_x, thr_y, thr_z, eor_x, eor_y, eor_z)))
					string_span_vectors = ','.join(map(str, (orthogonal_X_vector_x, orthogonal_X_vector_y, orthogonal_X_vector_z, orthogonal_Z_vector_x, orthogonal_Z_vector_y, orthogonal_Z_vector_z)))
					string_to_send = ','.join([string_plane, string_time, string_airport_local_coords, string_span_vectors])
					
					# Save the string_to_send to the non-active runway file
					if self.active_runway == 0:
						self.rwy_2_file.write(string_to_send + '\n')
					elif self.active_runway == 1:
						self.rwy_1_file.write(string_to_send + '\n')
					else:
						print 'ERROR! This should not happen!'
					
					self.record = False

		return 0.1
