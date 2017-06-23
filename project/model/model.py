#!/usr/bin/env python
# -*- coding: utf-8 -*-


#    Copyright © 2016, 2017 Oscar Franzén <oscarfranzen@yahoo.se>
#
#    This file is part of GCA Simulator.


import sys, time
from PySide import QtCore, QtGui, QtNetwork
import numpy as np
from airport import Airport


class MyModel(QtCore.QObject):


    new_plot_extracted = QtCore.Signal(object, object, object, object, object, object, object, object, object, object)
    new_airport = QtCore.Signal(object)
    new_communication_data = QtCore.Signal(object, object, object, object, object)
    new_connected_state = QtCore.Signal(object)
    connection_lost = QtCore.Signal()
    

    def __init__(self):
        super(MyModel, self).__init__()

        #self.UDP_IP = '172.20.10.2'
        self.UDP_IP = '192.168.1.88'
        self.UDP_SENDPORT = 5005
        self.UDP_RECEIVEPORT = 5006

        self.udp_receive_socket = QtNetwork.QUdpSocket(self)
        #self.udp_receive_socket.bind(QtNetwork.QHostAddress(self.UDP_IP), self.UDP_RECEIVEPORT, QtNetwork.QUdpSocket.DefaultForPlatform)
        self.udp_receive_socket.bind(self.UDP_RECEIVEPORT, QtNetwork.QUdpSocket.DefaultForPlatform)
        #self.udp_receive_socket.bind(QtNetwork.QHostAddress(self.UDP_IP), self.UDP_RECEIVEPORT, QtNetwork.QUdpSocket.ShareAddress|QtNetwork.QUdpSocket.ReuseAddressHint)
        
        self.udp_receive_socket.readyRead.connect(self.processPendingDatagrams)

        self.udp_send_socket = QtNetwork.QUdpSocket(self)     # Necessary???????



        self.airport = None         # 1 to 6 (not 0 to 5)?????????
        self.active_runway = None
        
        self.connected = False
        
        self.initTimeDelays()
        
        self.timer_senddata = QtCore.QTimer()
        self.timer_senddata.timeout.connect(self.sendDatagram)

        self.timer_connection_active = QtCore.QTimer()
        self.timer_connection_active.setSingleShot(True)
        self.timer_connection_active.timeout.connect(self.connectionLost)
        
        


    def readNewAirport(self, filename):
        try:
            self.airport = Airport(filename)
        except:
            print 'Some error occured trying to read ' + filename
        if self.airport: 
            self.new_airport.emit(self.airport)
            


    def probeXPlanePlugin(self):
        
        if self.connected:
            print 'closing connection'
            self.connected = False
            self.timer_senddata.stop()
            self.timer_connection_active.stop()
            self.new_connected_state.emit(self.connected)
            #self.new_plot_extracted.emit([], [], [], [], [], [], 0.0, (False, False), (False, False), (False, False))   # Why this?
        
        elif self.airport:
            print 'sending query'
            string_to_send = 'query'
            self.udp_send_socket.writeDatagram(string_to_send, QtNetwork.QHostAddress(self.UDP_IP), self.UDP_SENDPORT)

        else:
            print 'no airport chosen'



    def startCommunicatingWithXPlanePlugin(self):
        print 'starting communication'
        
        self.connected = True
        self.new_connected_state.emit(self.connected)
        self.timer_senddata.start(1000)
        self.initTimeDelays()



    def connectionLost(self):
        print 'lost connection'
        self.connected = False
        self.new_connected_state.emit(self.connected)
        #self.new_plot_extracted.emit([], [], [], [], [], [], 0.0, (False, False), (False, False), (False, False))       # Why?
        self.timer_senddata.stop()
        #self.connection_lost.emit()
        
        #print 'lost connection'




    def sendDatagram(self):
        
        list_of_strings = []
        
        list_of_strings.append(str(self.airport.runways[self.active_runway]['thr_lat']))
        list_of_strings.append(str(str(self.airport.runways[self.active_runway]['thr_lon']))            # This is the threshold coordinate for each runway
        list_of_strings.append(str(str(self.airport.runways[self.active_runway]['thr_el'] * 0.3048))    # El should be in meters, not feet.
        
        list_of_strings.append(str(self.airport.runways[self.active_runway]['eor_lat']))
        list_of_strings.append(str(str(self.airport.runways[self.active_runway]['eor_lon']))            # This is the threshold coordinate for each runway
        list_of_strings.append(str(str(self.airport.runways[self.active_runway]['eor_el'] * 0.3048))    # El should be in meters, not feet.
        
        
        
#        for each in self.airport.runways:
#            list_of_strings.append(str(each['lat']))
#            list_of_strings.append(str(each['lon']))            # This is the threshold coordinate for each runway
#            list_of_strings.append(str(each['el'] * 0.3048))    # El should be in meters, not feet.

        string_to_send = ','.join(list_of_strings)
        self.udp_send_socket.writeDatagram(string_to_send, QtNetwork.QHostAddress(self.UDP_IP), self.UDP_SENDPORT)  # TCP instead?

        self.latest_send_timestamp = time.time()
        
        


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
            
            
            

# ****************** FIX THIS MESS. I PREVIOUSLY SENT COORDS FROM ALL RUNWAYS EACH SECOND!!??!! WHY???????????

    def processPendingDatagrams(self):
        
        #print 'processing pending datagram'
        
        self.timer_connection_active.start(3000)
        
        self.latest_receive_timestamp = time.time()
        
        while self.udp_receive_socket.hasPendingDatagrams():
            datagram, host, port = self.udp_receive_socket.readDatagram(self.udp_receive_socket.pendingDatagramSize())
            try:
                # Python v3.
                datagram = str(datagram, encoding='ascii')
            except TypeError:
                # Python v2.
                pass

            if datagram == 'answer':
                print 'success, received an answer'
                self.startCommunicatingWithXPlanePlugin()
                
                #self.latest_receive_timestamp = time.time()
                
            else:

                #self.latest_receive_timestamp = time.time()
                
                # Do math on times here
                
                self.processTimeDelays()
                
                #print self.latest_receive_timestamp - self.latest_send_timestamp



                #print 'seem to be receiving an coord update'

                strings = datagram.split(',')

            #print strings

                float_points = map(float, strings)

            # Airplanes coords in local opengl coords
                self.coord_counter = 0
                self.airplane_point = np.array([float_points[self.coord_counter], float_points[self.coord_counter + 1], float_points[self.coord_counter + 2]])
                self.coord_counter += 3

            # Threshold points in opengl coords in threshold_points list for each pair of runways
                self.threshold_points = []
                for runway_counter in range( len(self.airport.runways) ):
                    self.threshold_points.append( np.array([float_points[self.coord_counter], float_points[self.coord_counter + 1], float_points[self.coord_counter + 2]] ) )
                    self.coord_counter += 3

                self.orthonormal_vectors = []
                for runway_counter in range(0, len(self.airport.runways), 2):
                # Unit vectors for each runway:
                # positive x-direction is directed from td to eor
                # positive y-direction is directed to the left when landing
                # positive z-direction is directed up
                    x_vector = np.array([float_points[self.coord_counter], float_points[self.coord_counter + 1], float_points[self.coord_counter + 2]])
                    z_vector = np.array([float_points[self.coord_counter + 3], float_points[self.coord_counter + 4], float_points[self.coord_counter + 5]])
                    x_norm = np.linalg.norm(x_vector)
                    x_unity_vector = x_vector / x_norm
                    z_norm = np.linalg.norm(z_vector)
                    z_unity_vector = z_vector / z_norm
                    y_unity_vector = np.cross(z_unity_vector, x_unity_vector)

                    self.orthonormal_vectors.append( [x_unity_vector, y_unity_vector, z_unity_vector] )
                    self.orthonormal_vectors.append( [-1.0*x_unity_vector, -1.0*y_unity_vector, z_unity_vector] )

                    self.coord_counter += 6

            # TD calculated only for active runway

                td = self.threshold_points[self.active_runway] + self.orthonormal_vectors[self.active_runway][0] * self.airport.runways[self.active_runway]['td']

            # Now calculate all relevant points as coordinates relative to the touchdown point

                airplane_relative_to_td = self.airplane_point - td
                x = np.dot(self.orthonormal_vectors[ self.active_runway ][0], airplane_relative_to_td)
                y = np.dot(self.orthonormal_vectors[ self.active_runway ][1], airplane_relative_to_td)
                z = np.dot(self.orthonormal_vectors[ self.active_runway ][2], airplane_relative_to_td)
                airplane_coordinate = np.array([x, y, z])

                thr_relative_to_td = self.threshold_points[self.active_runway] - td
                x = np.dot(self.orthonormal_vectors[ self.active_runway ][0], thr_relative_to_td)
                y = np.dot(self.orthonormal_vectors[ self.active_runway ][1], thr_relative_to_td)
                z = np.dot(self.orthonormal_vectors[ self.active_runway ][2], thr_relative_to_td)
                threshold_coordinate = np.array([x, y, z])

                if self.active_runway % 2 == 0:
                    eor_relative_to_td = self.threshold_points[self.active_runway + 1] - td
                else:
                    eor_relative_to_td = self.threshold_points[self.active_runway - 1] - td
                x = np.dot(self.orthonormal_vectors[ self.active_runway ][0], eor_relative_to_td)
                y = np.dot(self.orthonormal_vectors[ self.active_runway ][1], eor_relative_to_td)
                z = np.dot(self.orthonormal_vectors[ self.active_runway ][2], eor_relative_to_td)
                eor_coordinate = np.array([x, y, z])
                    
            # We will place the GCA right of runway when looking in the moving direction of the landing aircraft when landing on runway 1 (or 3 or 5).
            # It is placed some 100.0 meters from the centre of the airstrip.
                    
                if self.active_runway % 2 == 0:
                    gca_coordinate = (threshold_coordinate + eor_coordinate)/2 + np.array([0, -100.0, 4.0])         # The centre of the elevation antenna is about 4m from the ground 
                else:
                    gca_coordinate = (threshold_coordinate + eor_coordinate)/2 + np.array([0, 100.0, 4.0])

                mti_1_coordinate = gca_coordinate + np.array([750.0, 0.0, 5.0])
                mti_2_coordinate = gca_coordinate + np.array([-900.0, 0.0, 3.5])

                airplane_hit = (True, True)
                mti_1_hit = (True, True)
                mti_2_hit = (True, True)

                self.new_plot_extracted.emit(airplane_coordinate, threshold_coordinate, eor_coordinate, gca_coordinate, mti_1_coordinate, mti_2_coordinate, self.latest_receive_timestamp, airplane_hit, mti_1_hit, mti_2_hit)




    def quit(self):
        #self.udpSocket.leaveMulticastGroup(QtNetwork.QHostAddress(self.MCAST_GRP))
        QtGui.QApplication.quit()

