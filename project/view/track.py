#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    Copyright © 2016, 2017 Oscar Franzén <oscarfranzen@yahoo.se>
#
#    This file is part of GCA Simulator.

import numpy as np

class Track(object):
    
    max_historic_tracks = 15
    
    def __init__(self):
        
        self.list_of_coords = []
        
        self.elevation_plot_item = None
        self.azimuth_plot_item = None
        self.elevation_historic_plot_items = []
        self.azimuth_historic_plot_items = []

    def update(self, coord):
        if len(self.list_of_coords) == (self.max_historic_tracks + 1):
            
            del self.list_of_coords[-1]
            
        self.list_of_coords.insert(0, coord)
    
    def latest(self):
        if len(self.list_of_coords) > 0:
            return self.list_of_coords[0]
        else:
            return np.array([])
    
    def historic(self, number):
        if not number:
            return []
        if len(self.list_of_coords) == 1:
            return []
        elif len(self.list_of_coords) >= (number + 1):
            return self.list_of_coords[1:number + 1]
        else:
            return self.list_of_coords[1:]
    
    def clear(self):
        self.list_of_coords = []
        
    
    