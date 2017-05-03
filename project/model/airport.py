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

        self.words = s.split()
 
        runway_number = 0
        self.runways = []

        counter = 0

        while counter < len(self.words):

            if self.words[counter] == 'ICAO':
                self.icao = self.words[counter + 1]

            elif self.words[counter] == 'IATA':
                self.iata = self.words[counter + 1]

            elif self.words[counter][0:3] == 'RWY':
                runway_number = int(self.words[counter][3:4]) - 1
                self.runways.append({})
                self.runways[runway_number]['name'] = self.words[counter + 1]

            elif self.words[counter] == 'LON':
                self.runways[runway_number]['lon'] = float(self.words[counter + 1])

            elif self.words[counter] == 'LAT':
                self.runways[runway_number]['lat'] = float(self.words[counter + 1])

            elif self.words[counter] == 'EL':
                self.runways[runway_number]['el'] = float(self.words[counter + 1])

            elif self.words[counter] == 'TD':
                self.runways[runway_number]['td'] = float(self.words[counter + 1])

            elif self.words[counter] == 'GS':
                self.runways[runway_number]['gs'] = float(self.words[counter + 1])
                
            elif self.words[counter] == 'TRUE':
                self.runways[runway_number]['true'] = float(self.words[counter + 1])

            else:
                raise Exception('Error in airport file ' + filename)
                
            counter += 2

        

                



        

        


