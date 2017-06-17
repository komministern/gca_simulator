#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    Copyright © 2016, 2017 Oscar Franzén <oscarfranzen@yahoo.se>
#
#    This file is part of GCA Simulator.

import numpy as np
from plot import CorrelatedPlotItem, HistoricPlotItem
from label import ElevationLabel, AzimuthLabel

class Track(object):
    
    max_historic_tracks = 15
    
    ELEVATION = 0
    AZIMUTH = 1
    
    
    def __init__(self, scene):
        
        self.scene = scene
        
        self.list_of_coords = []
        self.list_of_hits = []
        self.list_of_extrapolated_coords = []
        
        self.elevation_plot_items = []
        self.azimuth_plot_items = []
        
        self.elevation_label = ElevationLabel(self.scene, self)
        self.azimuth_label = AzimuthLabel(self.scene, self)
        
        self.designated = False
        #self.whi_active = False
        
        self.callsign_string = 'ABC1234'
        self.size_string = 'M'

        self.velocity = 0.0
        self.elevation_deviation = 0.0
        self.azimuth_deviation = 0.0
        self.distance_to_td = 0.0



    def toggleDesignated(self):
        if self.designated:
            self.designated = False
            
            self.elevation_label.resetOffsets()
            self.azimuth_label.resetOffsets()

        else:
            self.designated = True
    
        self.draw(elevation=True, azimuth=True)

    
    
    def update(self, coord, hit):

        # This method is executed only when a new plot is processed. It is guaranteed that coord is
        # a valid coordinate.
        
        

        # Update list of plot coordinates
        if len(self.list_of_coords) == (self.max_historic_tracks + 1):
            del self.list_of_coords[-1]
        self.list_of_coords.insert(0, coord)
        
        # Update list of recorded hits for each antenna
        if len(self.list_of_hits) == (self.max_historic_tracks + 1):    # List for simulating missed targets in separate antennas
            del self.list_of_hits[-1]
        self.list_of_hits.insert(0, hit)
        
        # Extrapolate the next position
        pass
        
        # Calculate the varius label values
        self.calculateDistanceToTd()
        self.calculateVelocity()
        #self.calculateElevationDeviation()
        self.calculateAzimuthDeviation()

        
    def draw(self, elevation=False, azimuth=False):
        
        if len(self.list_of_coords) > 0:        # Do nothing if there are no plots to draw
        
            self.calculateElevationDeviation()          # This deviation is dependant on the glideslope!!! That is why it is executed here.
        
            self.elevation_label.update()
            self.azimuth_label.update()
        
            # Make labels visible (or the opposite)
            self.elevation_label.setVisible(self.designated)
            self.azimuth_label.setVisible(self.designated)
        
            # Draw the plots
            if elevation:
                self.drawElevationPlots()
            if azimuth:
                self.drawAzimuthPlots()
        
        
    def drawElevationPlots(self):

        # Remove all plots
        for each in self.elevation_plot_items:
            each.remove()
            del each

        self.elevation_plot_items = []
        
        # Draw new plots
        for i in range(len(self.list_of_coords)):
            
            if i <= self.scene.nhist:   # 1 + nhist
            
                elevation_point = self.scene.getElevationPoint(self.list_of_coords[i])
                
                if elevation_point != None:
                
                    x = elevation_point.x()
                    y = elevation_point.y()
            
                    if self.list_of_hits[i][self.ELEVATION] and (x < (self.scene.graphicsareawidth - self.scene.plot_radius)):
                    # If this is a hit in reasonable x range, draw a visible plot
            
                        if i == 0:
                            # This is a ordinary plot
                            self.elevation_plot_items.append(CorrelatedPlotItem(x, y, parent=None, scene=self.scene, parent_track=self))
                        elif (i > 0) and self.scene.hist_active:
                            # This is a historic plot
                            self.elevation_plot_items.append(HistoricPlotItem(x, y, parent=None, scene=self.scene, parent_track=self))


    def drawAzimuthPlots(self):

        # Remove all plots
        for each in self.azimuth_plot_items:
            each.remove()
            del each

        self.azimuth_plot_items = []
        
        # Draw new plots
        for i in range(len(self.list_of_coords)):
            
            if i <= self.scene.nhist:   # 1 + nhist
            
                azimuth_point = self.scene.getAzimuthPoint(self.list_of_coords[i])
                
                if azimuth_point != None:
                
                    x = azimuth_point.x()
                    y = azimuth_point.y()
            
                    if self.list_of_hits[i][self.AZIMUTH] and (x < (self.scene.graphicsareawidth - self.scene.plot_radius)):
                    # If this is a hit in reasonable x range, draw a visible plot
            
                        if i == 0:
                            # This is a ordinary plot
                            self.azimuth_plot_items.append(CorrelatedPlotItem(x, y, parent=None, scene=self.scene, parent_track=self))
                        elif (i > 0) and self.scene.hist_active:
                            # This is a historic plot
                            self.azimuth_plot_items.append(HistoricPlotItem(x, y, parent=None, scene=self.scene, parent_track=self))

            

    def clear(self):
        if self.designated:
            self.toggleDesignated()
        
        self.list_of_coords = []        # Could this empty list be a problem???!!!!????



    def calculateDistanceToTd(self):
        if len(self.list_of_coords[0]) == 3:
            meters = np.linalg.norm(self.list_of_coords[0])
            nautical_miles = meters / 1852.0
            self.distance_to_td = nautical_miles

            

    def calculateVelocity(self):
        if len(self.list_of_coords) >= 2:
            
            if len(self.list_of_coords[0]) == 3 and len(self.list_of_coords[1]) == 3:
                
                meters_per_second = np.linalg.norm(self.list_of_coords[1] - self.list_of_coords[0]) / self.scene.delta_t
                knots = meters_per_second * 1.943844 
                self.velocity = knots
            else:
                self.velocity = 0.0


            
                
    def calculateElevationDeviation(self):
        
        if len(self.list_of_coords[0]) == 3:
            plot_x = self.list_of_coords[0][0]
            plot_z = self.list_of_coords[0][2]
            preferred_height_in_m = -1.0 * plot_x * np.tan(self.scene.glideslope * np.pi / 180.0)
            deviation_from_glideslope_in_m = plot_z - preferred_height_in_m
            deviation_from_glideslope_in_feet = deviation_from_glideslope_in_m * 3.28084
            self.elevation_deviation = deviation_from_glideslope_in_feet
        
        
    
    def calculateAzimuthDeviation(self):

        if len(self.list_of_coords[0]) == 3:
            plot_y = self.list_of_coords[0][1]
            
            deviation_from_groundline_in_m = -1.0 * plot_y
            deviation_from_groundline_in_feet = deviation_from_groundline_in_m * 3.28084
            self.azimuth_deviation = deviation_from_groundline_in_feet
            
            