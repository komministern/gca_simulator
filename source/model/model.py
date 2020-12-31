#!/usr/bin/env python
# -*- coding: utf-8 -*-


#    Copyright © 2016, 2017 Oscar Franzén <oscarfranzen@yahoo.se>
#
#    This file is part of GCA Simulator.

import os
import sys
import time
import random
import shutil

import numpy as np
from PySide2 import QtCore, QtWidgets, QtGui, QtNetwork

from .airport import Airport
from .tracker import Tracker


from mycommonfunctions import path as mypath

class MyModel(QtCore.QObject):

    sim = 'dcs'
    #sim = 'xpl'

    new_plots_extracted = QtCore.Signal(object, object, object, object, object, object)
    new_airport = QtCore.Signal(object)
    new_communication_data = QtCore.Signal(object, object, object, object, object)
    new_flightsim_local_coord = QtCore.Signal(object)
    new_connected_state = QtCore.Signal(object)
    connection_lost = QtCore.Signal()
    demo_loop = QtCore.Signal()
    demo_init = QtCore.Signal()
    demo_end = QtCore.Signal()


    def initFileIO(self):

        self.application_directory = mypath.current_working_directory()
        self.user_home_directory = mypath.user_home_directory()

        # Try to find the Documents directory
        self.user_documents_directory = None

        if os.path.exists(os.path.join(self.user_home_directory, 'Documents')):
            self.user_documents_directory = os.path.join(self.user_home_directory, 'Documents')
        elif os.path.exists(os.path.join(self.user_home_directory, 'Dokument')):
            self.user_documents_directory = os.path.join(self.user_home_directory, 'Dokument')

        if self.user_documents_directory != None:
            self.local_data_root_directory = os.path.join(self.user_documents_directory, 'GCA Simulator Data')
        else:
            self.local_data_root_directory = os.path.join(self.user_home_directory, 'GCA Simulator Data')

        # self.local_data_config_directory = self.local_data_root_directory
        # self.local_data_log_directory = os.path.join(self.local_data_root_directory, 'logs')
        self.local_data_recordings_directory = os.path.join(self.local_data_root_directory, 'recordings')
        self.local_data_airports_directory = os.path.join(self.local_data_root_directory, 'airports')
        self.local_data_plugins_directory = os.path.join(self.local_data_root_directory, 'plugins')
        self.local_data_dcs_plugin_directory = os.path.join(self.local_data_plugins_directory, 'dcs')
        self.local_data_xplane_plugin_directory = os.path.join(self.local_data_plugins_directory, 'xplane')

        self.default_resources_directory = os.path.join(self.application_directory, 'resources')
        self.default_recordings_directory = os.path.join(self.default_resources_directory, 'recordings')
        self.default_airports_directory = os.path.join(self.default_resources_directory, 'airports')
        self.default_plugins_directory = os.path.join(self.default_resources_directory, 'plugins')
        self.default_dcs_plugin_directory = os.path.join(self.default_plugins_directory, 'dcs')
        self.default_xplane_plugin_directory = os.path.join(self.default_plugins_directory, 'xplane')
        self.default_sounds_directory = os.path.join(self.default_resources_directory, 'sounds')

        # Initialize directories and stuff
        
        if not os.path.exists(self.local_data_root_directory):
            os.mkdir(self.local_data_root_directory)

        # if not os.path.exists(self.local_data_log_directory):
        #     os.mkdir(self.local_data_log_directory)

        # RECORDINGS
        if not os.path.exists(self.local_data_recordings_directory):
            os.mkdir(self.local_data_recordings_directory)
        shutil.copyfile(os.path.join(self.default_recordings_directory, 'demo.rec'), os.path.join(self.local_data_recordings_directory, 'demo.rec'))

        # AIRPORTS
        if not os.path.exists(self.local_data_airports_directory):
            os.mkdir(self.local_data_airports_directory)
        shutil.copyfile(os.path.join(self.default_airports_directory, 'batumi.apt'), os.path.join(self.local_data_airports_directory, 'batumi.apt'))
        shutil.copyfile(os.path.join(self.default_airports_directory, 'readme.txt'), os.path.join(self.local_data_airports_directory, 'readme.txt'))

        # PLUGINS
        if not os.path.exists(self.local_data_plugins_directory):
            os.mkdir(self.local_data_plugins_directory)
        
        if os.path.exists(self.local_data_dcs_plugin_directory):
            shutil.rmtree(self.local_data_dcs_plugin_directory)
        shutil.copytree(self.default_dcs_plugin_directory, self.local_data_dcs_plugin_directory)
        # if os.path.exists(self.local_data_xplane_plugin_directory):
        #     shutil.rmtree(self.local_data_xplane_plugin_directory)
        # shutil.copytree(self.default_xplane_plugin_directory, self.local_data_xplane_plugin_directory)

       


    def __init__(self):
        super(MyModel, self).__init__()

        self.initFileIO()

        self.tracker = Tracker(self)

        self.working_directory = mypath.current_working_directory()
        print(self.working_directory)
        self.default_resources_directory = os.path.join(self.working_directory, 'resources')
        self.default_airports_directory = os.path.join(self.default_resources_directory, 'airports')
        self.default_recordings_directory = os.path.join(self.default_resources_directory, 'recordings')


        self.runway_password = 'plt'
        self.radar_mode_password = 'plt'
        self.radar_control_password = 'plt'
        self.ppi_password = 'plt'


        #self.UDP_IP = '172.20.10.2'
        #self.UDP_IP = '127.0.0.1'
        #self.UDP_IP = '192.168.1.88'
        self.UDP_SENDPORT = 5005
        self.UDP_RECEIVEPORT = 5006

        self.udp_receive_socket = QtNetwork.QUdpSocket(self)
        #self.udp_receive_socket.bind(QtNetwork.QHostAddress(self.UDP_IP), self.UDP_RECEIVEPORT, QtNetwork.QUdpSocket.DefaultForPlatform)
        self.udp_receive_socket.bind(self.UDP_RECEIVEPORT, QtNetwork.QUdpSocket.DefaultForPlatform)
        #self.udp_receive_socket.bind(QtNetwork.QHostAddress(self.UDP_IP), self.UDP_RECEIVEPORT, QtNetwork.QUdpSocket.ShareAddress|QtNetwork.QUdpSocket.ReuseAddressHint)
        
        self.udp_receive_socket.readyRead.connect(self.processPendingDatagrams)

        self.udp_send_socket = QtNetwork.QUdpSocket(self)     # Necessary???????


        self.airport = None
        self.active_runway = None
        
        self.sending = False
        self.connected = False
        self.recording = False
        self.demo_mode = False
        self.demo_has_restarted = False



        self.record_file = None
        self.latest_airport_filename = None
        
        self.initTimeDelays()
        
        self.timer_senddata = QtCore.QTimer()
        self.timer_senddata.timeout.connect(self.sendDatagram)

        self.timer_connection_active = QtCore.QTimer()
        self.timer_connection_active.setSingleShot(True)
        self.timer_connection_active.timeout.connect(self.connectionLost)

        self.azantelev = None
        self.elantazim = None

        self.rain_mode = False

        self.radiating = False
        
        self.wf_counter = 0

        self.time_stamp_radiate_on = 0.0


        

    def readNewAirport(self, filename):
        #try:
        self.airport = Airport(filename)
        #except:
        #    print('Some error occured trying to read ' + filename)
        if self.airport: 
            self.new_airport.emit(self.airport)
            self.present_airport_filename = filename
            


    def probeXPlanePlugin(self):
        if self.connected:
            print('closing connection')
            self.connected = False
            self.timer_senddata.stop()
            self.timer_connection_active.stop()
            self.new_connected_state.emit(self.connected)
        
        elif self.airport:
            print('sending query')
            string_to_send = 'query'
            self.udp_send_socket.writeDatagram(string_to_send, QtNetwork.QHostAddress(self.UDP_IP), self.UDP_SENDPORT)
        else:
            print('no airport chosen')


    def startSendingToPlugin(self):
        print('starting to send')
        self.timer_senddata.start(250)
        self.initTimeDelays()

    def stopSendingToPlugin(self):
        print('stopping to send')
        self.timer_senddata.stop()
        self.timer_connection_active.stop()
        #self.connectionLost()


    #def startCommunicatingWithXPlanePlugin(self):
    #    print 'starting communication'
    #    self.connected = True
    #    self.new_connected_state.emit(self.connected)
    #    self.timer_senddata.start(1000)
    #    self.initTimeDelays()



    def connectionLost(self):
        print('lost connection')
        self.connected = False
        self.new_connected_state.emit(self.connected)
        #self.timer_senddata.stop()
        #self.connection_lost.emit()





    def sendDatagram(self):
        
        if not self.demo_mode:
        
            if self.sim == 'xpl':

                list_of_strings = []

                if self.record == True:
                    list_of_strings.append('record')
                    list_of_strings.append(str(self.active_runway))
        
                list_of_strings.append(str(self.airport.runways[self.active_runway]['thr_lat']))
                list_of_strings.append(str(self.airport.runways[self.active_runway]['thr_lon']))            # This is the threshold coordinate for each runway
                list_of_strings.append(str(self.airport.runways[self.active_runway]['thr_el'] * 0.3048))    # El should be in meters, not feet.
        
                list_of_strings.append(str(self.airport.runways[self.active_runway]['eor_lat']))
                list_of_strings.append(str(self.airport.runways[self.active_runway]['eor_lon']))            # This is the threshold coordinate for each runway
                list_of_strings.append(str(self.airport.runways[self.active_runway]['eor_el'] * 0.3048))    # El should be in meters, not feet.

                string_to_send = ','.join(list_of_strings)
                self.udp_send_socket.writeDatagram(string_to_send.encode(), QtNetwork.QHostAddress(self.UDP_IP), self.UDP_SENDPORT)  # TCP instead?

            elif self.sim == 'dcs':

                #print(self.airport.runways)
                #print(self.active_runway)

                list_of_strings = []

                for runway_number in self.airport.runways:  # Order??????!!!!!!!!!!!
                    list_of_strings.append(str(self.airport.runways[runway_number]['thr_lat']))
                    list_of_strings.append(str(self.airport.runways[runway_number]['thr_lon']))              # This is the threshold coordinate for each runway
                    list_of_strings.append( format(self.airport.runways[runway_number]['thr_el'] * 0.3048, '.1f') )      # El should be in meters, not feet.

                    list_of_strings.append(str(self.airport.runways[runway_number]['eor_lat']))
                    list_of_strings.append(str(self.airport.runways[runway_number]['eor_lon']))              # This is the threshold coordinate for each runway
                    list_of_strings.append(format(self.airport.runways[runway_number]['eor_el'] * 0.3048, '.1f'))      # El should be in meters, not feet.

                string_to_send = ','.join(list_of_strings)
                #print('s: ' + string_to_send)
                self.udp_send_socket.writeDatagram(string_to_send.encode(), QtNetwork.QHostAddress(self.UDP_IP), self.UDP_SENDPORT)  # TCP instead?


        elif self.demo_mode:
            
            next_message = self.demo_file.readline().replace('\n', '')
            
            if not next_message:
                self.demo_file.seek(0)
                discard_message = self.demo_file.readline()
                next_message = self.demo_file.readline().replace('\n', '')
                self.demo_has_restarted = True
                self.demo_loop.emit()

            #print 'sending message'
            self.udp_send_socket.writeDatagram(next_message.encode(), QtNetwork.QHostAddress(self.UDP_IP), self.UDP_RECEIVEPORT)

        self.latest_send_timestamp = time.time()
        
        

    def initDemoMode(self, filename):
        
        self.demo_file = open(filename, 'r')
        
        airport_filename = self.demo_file.readline().replace('\n', '')

        #print airport_filename

        self.readNewAirport(os.path.join(self.local_data_airports_directory, airport_filename))
        
        self.demo_mode = True
        
        #self.active_runway = None
        
        #self.readNewAirport(self.present_airport_filename)

        #self.startCommunicatingWithXPlanePlugin()
        self.UDP_IP = '127.0.0.1'

        self.time_stamp_radiate_on = time.time()

        self.demo_init.emit()

        self.startSendingToPlugin()



    def exitDemoMode(self):

        self.stopSendingToPlugin()
        
        self.demo_mode = False
        
        self.demo_file.close()
        
        self.connectionLost()




    def initTimeDelays(self):
        self.message_counter = 0
        self.delays = []




    def processTimeDelays(self):
        self.message_counter += 1
        latest_delay = self.latest_receive_timestamp - self.latest_send_timestamp
        n = 10
        if len(self.delays) == n:
            del self.delays[-1]
        self.delays.insert(0, latest_delay)
        array = np.array(self.delays)
        mean = array.mean()
        stddev = array.std()
        self.new_communication_data.emit(self.message_counter, latest_delay, mean, stddev, self.connected)
            


    def processPendingDatagrams(self):

        #print 'received a message'

        self.timer_connection_active.start(5000)
        
        #self.latest_receive_timestamp = time.time()
        
        while self.udp_receive_socket.hasPendingDatagrams():

            self.latest_receive_timestamp = time.time()
            
            datagram, host, port = self.udp_receive_socket.readDatagram(self.udp_receive_socket.pendingDatagramSize())
            
            #try:
                # Python v3.
            #    datagram = str(datagram, encoding='ascii')
            #except TypeError:
                # Python v2.
            #    pass

            received_string = datagram.data().decode()

            #print(type(received_string))

            if True:

                # Do math on times here
                self.processTimeDelays()

                #strings = datagram.split(',')
                strings = received_string.split(',')

                #print(strings)


                if strings[0] == 'dcs':

                    if not self.connected:
                        self.connected = True
                        self.new_connected_state.emit(self.connected)

                    time_stamp = float(strings[1])

                    thr_rwy = {}
                    eor_rwy = {}

                    i = 2
                    for runway_number in self.airport.runways:

                        if 'dcs_thr_x' in self.airport.runways[runway_number]:

                            thr_rwy[runway_number] = np.array((self.airport.runways[runway_number]['dcs_thr_x'], self.airport.runways[runway_number]['dcs_thr_y'], self.airport.runways[runway_number]['dcs_thr_z']))
                            eor_rwy[runway_number] = np.array((self.airport.runways[runway_number]['dcs_eor_x'], self.airport.runways[runway_number]['dcs_eor_y'], self.airport.runways[runway_number]['dcs_eor_z']))
                            #thr_rwy[runway_number] = np.array([-355130.3, 12.0, 616436.1])
                            #eor_rwy[runway_number] = np.array([-356537.8, 12.0, 618404.1])

                            # This dirty solution must be applied as the accurace in the DCS coordinate conversion functions is too poor.

                        else:

                            thr_rwy[runway_number] = np.array([float(coord) for coord in strings[i:i+3]])
                            eor_rwy[runway_number] = np.array([float(coord) for coord in strings[i+3:i+6]])

                        i += 6

                    aircrafts = {}
                    while i < len(strings):
                        #aircrafts[strings[i]] = np.array(map(float, strings[i+1:i+4])) #Every track starts with an identifier string named by the flight simulator, followed by three coordinates
                        #print('aircraft_xyz:')
                        #print(np.array([float(coord) for coord in strings[i+1:i+4]]))
                        aircrafts[strings[i]] = np.array([float(coord) for coord in strings[i+1:i+4]])
                        i += 4

                    if len(aircrafts) == 1 and not self.demo_mode:
                        # Show coordinates in status window, but only if there is only one aircraft in range (to avoid ambiguity)!!!
                        self.new_flightsim_local_coord.emit(aircrafts[strings[i - 4]])
                        
                    

                    # x is north
                    # y is up
                    # z is east

                    thr = thr_rwy[self.active_runway]
                    eor = eor_rwy[self.active_runway]

                    #print(thr)
                    #print(type(thr))

                    orthonormal_vectors = {}

                    # Unit vectors for the active runway:
                    # positive u-direction is directed from thr to eor
                    # positive v-direction is directed to the left when landing
                    # positive w-direction is directed up
                    
                    orthonormal_vectors['u'] = (eor - thr) / np.linalg.norm(eor - thr)
                    orthonormal_vectors['w'] = np.array([0.0, 1.0, 0.0])                                        # Hmmmm, is this vector actually pointing straight upwards??????? YES IT IS!!!!
                    orthonormal_vectors['v'] = np.cross(orthonormal_vectors['w'], orthonormal_vectors['u'])

                    td = thr + orthonormal_vectors['u'] * self.airport.runways[self.active_runway]['td']

                    # Now calculate all relevant points as coordinates relative to the touchdown point

                    thr_relative_to_td = thr - td
                    x = np.dot(orthonormal_vectors['u'], thr_relative_to_td)
                    y = np.dot(orthonormal_vectors['v'], thr_relative_to_td)
                    z = np.dot(orthonormal_vectors['w'], thr_relative_to_td)
                    thr_coordinate = np.array([x, y, z])
                    #print('thr coordinate:')
                    #print(thr_coordinate)

                    eor_relative_to_td = eor - td
                    x = np.dot(orthonormal_vectors['u'], eor_relative_to_td)
                    y = np.dot(orthonormal_vectors['v'], eor_relative_to_td)
                    z = np.dot(orthonormal_vectors['w'], eor_relative_to_td)
                    eor_coordinate = np.array([x, y, z])
                    #print('eor coordinate:')
                    #print(eor_coordinate)

                    # We will place the GCA right of runway when looking in the moving direction of the landing aircraft when landing on runway 1 (or 3 or 5).
                    # It is placed some 100.0 meters from the centre of the airstrip.
                    
                    if self.active_runway % 2 == 0:
                        gca_coordinate = (thr_coordinate + eor_coordinate)/2 + np.array([0, 75.0, 4.0])         # The centre of the elevation antenna is about 4m from the ground 
                        gca_el_coordinate = (thr_coordinate + eor_coordinate)/2 + np.array([0, 75.0, 3.0])      # The centre of the el elevation antenna is about 3m from the ground
                        gca_az_coordinate = (thr_coordinate + eor_coordinate)/2 + np.array([0, 75.0, 5.0])      # The centre of the az elevation antenna is about 5m from the ground
                    else:
                        gca_coordinate = (thr_coordinate + eor_coordinate)/2 + np.array([0, -75.0, 4.0])
                        gca_el_coordinate = (thr_coordinate + eor_coordinate)/2 + np.array([0, -75.0, 3.0])      # The centre of the el elevation antenna is about 3m from the ground
                        gca_az_coordinate = (thr_coordinate + eor_coordinate)/2 + np.array([0, -75.0, 5.0])      # The centre of the az elevation antenna is about 5m from the ground


                    target_coordinates = {}

                    mti_coordinate = gca_coordinate + np.array([-800.0, 0.0, 0.5])      # MTI 900m from GCA, and the dish on 4.5m height (GCA height is 4.0m)

                    target_coordinates['mti'] = self.scramble_coordinate(mti_coordinate)

                    for aircraft_name in aircrafts:
                        plane_relative_to_td = aircrafts[aircraft_name] - td
                        x = np.dot(orthonormal_vectors['u'], plane_relative_to_td)
                        y = np.dot(orthonormal_vectors['v'], plane_relative_to_td)
                        z = np.dot(orthonormal_vectors['w'], plane_relative_to_td)
                        aircraft_coordinate = np.array([x, y, z])
                        #print('aircraft coordinate:')
                        #print(aircraft_coordinate)
                        target_coordinates[aircraft_name] = self.scramble_coordinate(aircraft_coordinate)


                    target_hits = {}
                    filtered_target_coordinates = {}

                    for aircraft_name in target_coordinates:

                        coord_rel_to_gca = target_coordinates[aircraft_name] - gca_coordinate

                        if coord_rel_to_gca[0] < 0:     # Only bother if the target is in front of the radar
                            
                            distance_to_aircraft = np.linalg.norm(coord_rel_to_gca)         # Unit: m
                            distance_to_aircraft_nm = self.nm(distance_to_aircraft)
                            d = distance_to_aircraft_nm

                            target_in_waveform_range = False

                            #print(coord_rel_to_gca)

                            if self.wf_counter == 0:
                                if d > 3.0 and d < 20.0:
                                    target_in_waveform_range = True

                            elif self.wf_counter == 1:
                                if d > 2.0 and d < 7.5:
                                    target_in_waveform_range = True
                                elif d > 10.5 and d < 16.0:
                                    target_in_waveform_range = True
                                elif d > 19.0 and d < 24.5:
                                    target_in_waveform_range = True

                            elif self.wf_counter == 2:
                                if d > 3.0 and d < 11.0:
                                    target_in_waveform_range = True
                                elif d > 17.0 and d < 25.0:
                                    target_in_waveform_range = True

                            elif self.wf_counter == 3:
                                if d > 0.1 and d < 5.5:
                                    target_in_waveform_range = True
                                elif d > 6.0 and d < 11.5:
                                    target_in_waveform_range = True

                            if target_in_waveform_range:
                                el_hit = self.elevation_hit( target_coordinates[aircraft_name], gca_el_coordinate )
                                az_hit = self.azimuth_hit( target_coordinates[aircraft_name], gca_az_coordinate )

                                # if el_hit or az_hit:
                                target_hits[aircraft_name] = (el_hit, az_hit)     # el, az
                                filtered_target_coordinates[aircraft_name] = target_coordinates[aircraft_name]
                            # else:
                            #     target_hits[aircraft_name] = (False, False)
                            #     if aircraft_name == 'mti':
                            #         print('------------------------------------------')

                    
                    #if len(filtered_target_coordinates) > 0:
                    self.tracker.process_hits(time_stamp, thr_coordinate, eor_coordinate, gca_el_coordinate, filtered_target_coordinates, target_hits)
                    # self.new_plots_extracted.emit(time_stamp, thr_coordinate, eor_coordinate, gca_el_coordinate, filtered_target_coordinates, target_hits)
                    

                if not self.recording and self.record_file != None:
                    self.record_file.close()
                    self.record_file = None

                elif self.recording and self.record_file == None:
                    #self.record_file = open('./resources/recordings/new_recording.txt', 'w')
                    self.record_file = open(os.path.join(self.local_data_recordings_directory, 'newrecord.rec', 'w'))
                    

                    head, tail = os.path.split(self.airport.filename)
                    self.record_file.write(tail + '\n')         # Save ONLY the actual filename, not the complete path!!!!!!!!!!!!!!

                if self.recording:
                    self.record_file.write(received_string + '\n')
                    #self.record_file.write(datagram + '\n')
                    #print(datagram + '\n')

                self.wf_counter += 1
                if self.wf_counter > 3:
                    self.wf_counter = 0
                    



    def scramble_coordinate(self, coordinate):
        
        std_dev_theta = 0.0003     # Side angle
        std_dev_fi = 0.0002        # Vertical angle

        delta_theta = np.random.normal(scale=std_dev_theta)
        delta_fi = np.random.normal(scale=std_dev_fi)

        delta_y = coordinate[0] * np.tan(delta_theta)
        delta_z = coordinate[0] * np.tan(delta_fi)

        return coordinate + np.array([0.0, delta_y, delta_z])
        

        


        



    def elevation_hit(self, coord, gca_coord):
        
        elantazim = -self.elantazim

        p_normal = 0.995
        
        if self.rain_mode:
            r_full_prb = 13.0
            r_zero_prb = 16.0 
        else:
            r_full_prb = 16.0
            r_zero_prb = 19.0      
        
        fi_up_full_prb = 7.0
        fi_up_zero_prb = 7.2
        
        fi_down_full_prb = -1.0
        fi_down_zero_prb = -1.2
        
        theta_left_full_prb = 14.0 + elantazim
        theta_left_zero_prb = 19.0 + elantazim

        theta_right_full_prb = -14.0 + elantazim
        theta_right_zero_prb = -19.0 + elantazim

        coord_rel_to_gca = coord - gca_coord

        #r_xy = np.linalg.norm(coord_rel_to_gca[:2])        # Distance without height
        r = np.linalg.norm(coord_rel_to_gca)               # Distance with height
        theta = np.arctan(coord_rel_to_gca[1]/coord_rel_to_gca[0])    # Side angle (positive is ro the LEFT when watching from the GCA towards the mti reflector)
        fi = np.arcsin(coord_rel_to_gca[2]/r)              # Height angle (positive is up)
    

        if coord_rel_to_gca[0] > 0.0 or self.nm(r) > r_zero_prb or self.deg(theta) > theta_left_zero_prb or self.deg(theta) < theta_right_zero_prb or self.deg(fi) > fi_up_zero_prb:
            elevation_hit = False
            #print 'elevation probability = 0'
        
        else:
            
            p_hit = p_normal

            if self.nm(r) > r_full_prb:
                p_hit *= self.f(self.nm(r), r_full_prb, r_zero_prb)
            
            if self.deg(fi) > fi_up_full_prb:
                p_hit *= self.f(self.deg(fi), fi_up_full_prb, fi_up_zero_prb)

            if self.deg(theta) > theta_left_full_prb:
                p_hit *= self.f(self.deg(theta), theta_left_full_prb, theta_left_zero_prb)
            elif self.deg(theta) < theta_right_full_prb:
                p_hit *= self.f(self.deg(theta), theta_right_full_prb, theta_right_zero_prb)
            
            if random.random() < p_hit:
                elevation_hit = True
            else:
                elevation_hit = False
            
        return elevation_hit
        #return True


    def azimuth_hit(self, coord, gca_coord):
        
        elantazim = -self.elantazim
        azantelev = self.azantelev

        p_normal = 0.997
        
        if self.rain_mode:
            r_full_prb = 12.0
            r_zero_prb = 22.0
        else:   
            r_full_prb = 15.0
            r_zero_prb = 22.0      
        
        #fi_up_full_prb = azantelev + 5.0
        #fi_up_zero_prb = azantelev + 10.1
        
        #fi_down_full_prb = azantelev - 0.0
        #fi_down_zero_prb = azantelev - 0.1

        fi_up_full_prb = azantelev + 5.0
        fi_up_zero_prb = azantelev + 10.0
        
        fi_down_full_prb = azantelev - 1.95
        fi_down_zero_prb = azantelev - 10.0

        theta_left_full_prb = 15.0 + elantazim
        theta_left_zero_prb = 15.2 + elantazim

        theta_right_full_prb = -15.0 + elantazim
        theta_right_zero_prb = -15.2 + elantazim

        coord_rel_to_gca = coord - gca_coord

        #r_xy = np.linalg.norm(coord_rel_to_gca[:2])        # Distance without height
        
        r = np.linalg.norm(coord_rel_to_gca)               # Distance with height
        theta = np.arctan(coord_rel_to_gca[1]/coord_rel_to_gca[0])    # Side angle (positive is ro the LEFT when watching from the GCA towards the mti reflector)
        fi = np.arcsin(coord_rel_to_gca[2]/r)              # Height angle (positive is up)
        

        if coord_rel_to_gca[0] > 0.0 or self.nm(r) > r_zero_prb or self.deg(theta) > theta_left_zero_prb or self.deg(theta) < theta_right_zero_prb or self.deg(fi) > fi_up_zero_prb or self.deg(fi) < fi_down_zero_prb:
            azimuth_hit = False
            #print 'azimuth probability = 0'
        
        else:
            
            p_hit = p_normal

            #print 'theta ' + str(theta)
            #print 'fi ' + str(fi)
            #print 'r ' + str(r)

            if self.nm(r) > r_full_prb:
                p_hit *= self.f(self.nm(r), r_full_prb, r_zero_prb)
            #    print 'r ' + str(p_hit)

            if self.deg(fi) > fi_up_full_prb:
                p_hit *= self.f(self.deg(fi), fi_up_full_prb, fi_up_zero_prb)
            #    print 'fi_up ' + str(p_hit)
            elif self.deg(fi) < fi_down_full_prb:
                p_hit *= self.f(self.deg(fi), fi_down_full_prb, fi_down_zero_prb)
            #    print 'fi_down ' + str(p_hit)

            if self.deg(theta) > theta_left_full_prb:
                p_hit *= self.f(self.deg(theta), theta_left_full_prb, theta_left_zero_prb)
            #    print 'theta_left ' + str(p_hit)
            elif self.deg(theta) < theta_right_full_prb:
                p_hit *= self.f(self.deg(theta), theta_right_full_prb, theta_right_zero_prb)
            #    print 'theta_right ' + str(p_hit)
           
            if random.random() < p_hit:
                azimuth_hit = True
            else:
                azimuth_hit = False
            
        return azimuth_hit
        #return True

    
    def f(self, x, x_full_prb, x_zero_prb):
        return (x_zero_prb - x) / (x_zero_prb - x_full_prb)
        
    def deg(self, radians):
        return radians*180.0/np.pi
        
    def nm(self, meters):
        return meters/1852.0

    def quit(self):
        QtWidgets.QApplication.quit()



            

