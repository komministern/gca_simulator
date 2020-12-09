#!/usr/bin/env python
# -*- coding: utf-8 -*-


#    Copyright © 2016, 2017 Oscar Franzén <oscarfranzen@yahoo.se>
#
#    This file is part of GCA Simulator.


class Airport(object):

    def __init__(self, filename):
        super(Airport, self).__init__()

        with open(filename) as f:
            s = f.read()
        f.close()

        self.filename = filename

        self.words = s.split()
 
        self.runway_number = None
        self.runways = {}

        counter = 0



        while counter < len(self.words):

            if self.words[counter] == 'ICAO':
                self.icao = self.words[counter + 1]

            elif self.words[counter] == 'IATA':
                self.iata = self.words[counter + 1]

            elif self.words[counter][0:3] == 'RWY':

                runway_number = int(self.words[counter][3:4])
                self.runways[runway_number] = {}
                self.runways[runway_number]['name'] = self.words[counter + 1]

            elif self.words[counter] == 'THR_LON':
                self.runways[runway_number]['thr_lon'] = float(self.words[counter + 1])

            elif self.words[counter] == 'THR_LAT':
                self.runways[runway_number]['thr_lat'] = float(self.words[counter + 1])

            elif self.words[counter] == 'THR_EL':
                self.runways[runway_number]['thr_el'] = float(self.words[counter + 1])
                
            elif self.words[counter] == 'EOR_LON':
                self.runways[runway_number]['eor_lon'] = float(self.words[counter + 1])

            elif self.words[counter] == 'EOR_LAT':
                self.runways[runway_number]['eor_lat'] = float(self.words[counter + 1])

            elif self.words[counter] == 'EOR_EL':
                self.runways[runway_number]['eor_el'] = float(self.words[counter + 1])
            
            elif self.words[counter] == 'TD':
                self.runways[runway_number]['td'] = float(self.words[counter + 1])

            elif self.words[counter] == 'GS':
                self.runways[runway_number]['gs'] = float(self.words[counter + 1])
                
            elif self.words[counter] == 'TRUE':
                self.runways[runway_number]['true'] = float(self.words[counter + 1])

            elif self.words[counter] == 'DCS_THR_X':
                self.runways[runway_number]['dcs_thr_x'] = float(self.words[counter + 1])
                #print('FITA ' + self.words[counter + 1])
            
            elif self.words[counter] == 'DCS_THR_Y':
                self.runways[runway_number]['dcs_thr_y'] = float(self.words[counter + 1])
                #print('KUK')
            
            elif self.words[counter] == 'DCS_THR_Z':
                self.runways[runway_number]['dcs_thr_z'] = float(self.words[counter + 1])
            
            elif self.words[counter] == 'DCS_EOR_X':
                self.runways[runway_number]['dcs_eor_x'] = float(self.words[counter + 1])
            
            elif self.words[counter] == 'DCS_EOR_Y':
                self.runways[runway_number]['dcs_eor_y'] = float(self.words[counter + 1])
            
            elif self.words[counter] == 'DCS_EOR_Z':
                self.runways[runway_number]['dcs_eor_z'] = float(self.words[counter + 1])

            else:
                raise Exception('Error in airport file ' + filename)
                
            counter += 2

        

                



        

        


