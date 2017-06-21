#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    Copyright © 2016, 2017 Oscar Franzén <oscarfranzen@yahoo.se>
#
#    This file is part of GCA Simulator.

from PySide import QtGui, QtCore
import numpy as np
from plot import CorrelatedPlotItem, HistoricPlotItem, WhiPlotItem
from label import ElevationLabel, AzimuthLabel, WhiLabel

class Track(QtCore.QObject):
    
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
        self.whi_plot_item = None
        
        self.elevation_label = ElevationLabel(self.scene, self)
        self.azimuth_label = AzimuthLabel(self.scene, self)
        self.whi_label = WhiLabel(self.scene, self)
        
        #self.designated = False
        #self.whi_active = False
        
        self.callsign_string = ''
        self.size_string = 'M'          # Default value I guess!?!

        self.velocity = 0.0
        self.elevation_deviation = 0.0
        self.azimuth_deviation = 0.0
        self.distance_to_td = 0.0


    def designated(self):
        return (self in self.scene.designated_tracks)

    def active_designated(self):
        if len(self.scene.designated_tracks) > 0:
            return (self == self.scene.designated_tracks[0])
        else:
            return False


    def toggleDesignated(self):
        
        if self.active_designated():
            self.scene.designated_tracks.remove(self)
            self.draw(elevation=True, azimuth=True, whi=True)
            #self.drawWhiPlot()
            self.elevation_label.resetOffsets()
            self.azimuth_label.resetOffsets()
            self.resetCallsign()
            
            if len(self.scene.designated_tracks) > 0:
                self.scene.designated_tracks[0].setActive()
                self.scene.designated_tracks[0].draw(elevation=True, azimuth=True, whi=True)
                #self.scene.designated_tracks[0].drawWhiPlot()

        elif self.designated():
            self.scene.designated_tracks.remove(self)
            self.draw(elevation=True, azimuth=True)

            self.elevation_label.resetOffsets()
            self.azimuth_label.resetOffsets()
            self.resetCallsign()

        else:
            self.scene.designated_tracks.insert(0, self)
            self.setActive()
            self.draw(elevation=True, azimuth=True, whi=True)
            #self.drawWhiPlot()
            
            if len(self.scene.designated_tracks) > 1:
                self.scene.designated_tracks[1].setPassive()
                self.scene.designated_tracks[1].draw(elevation=True, azimuth=True, whi=True)
                #self.scene.designated_tracks[1].drawWhiPlot()

    
    
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
        self.calculateAzimuthDeviation()


    def setActive(self):
        self.elevation_label.setActiveColors()
        self.azimuth_label.setActiveColors()
        self.elevation_label.setActiveZValue()
        self.azimuth_label.setActiveZValue()
        
    def setPassive(self):
        self.elevation_label.setPassiveColors()
        self.azimuth_label.setPassiveColors()
        self.elevation_label.setPassiveZValue()
        self.azimuth_label.setPassiveZValue()




    # Structure the drawing of the tracks
    # Break out the remove plots as separate methods
    


    def draw(self, elevation=False, azimuth=False, whi=False):
        
        if len(self.list_of_coords) > 0:        # Do nothing if there are no plots to draw
        
            self.calculateElevationDeviation()          # This deviation is dependant on the glideslope!!! That is why it is executed here.
        
            self.elevation_label.update()
            self.azimuth_label.update()
        
            # Make labels visible (or the opposite)
            self.elevation_label.setVisible(self.designated() and self.scene.radiating)
            self.azimuth_label.setVisible(self.designated() and self.scene.radiating)
            self.whi_label.setVisible(self.active_designated() and self.scene.radiating)          # More work needed here!!!!!!!!!!!!

            # Remove the old plots
            if elevation:
                self.removeElevationPlots()
            if azimuth:
                self.removeAzimuthPlots()
            if whi:
                self.removeWhiPlot()

            # Draw the new plots
            if self.scene.radiating:
                if elevation:
                    self.drawElevationPlots()
                if azimuth:
                    self.drawAzimuthPlots()
                if whi and self.active_designated():
                    self.drawWhiPlot()
                
    
    def removeElevationPlots(self):
        # Remove all plots
        for each in self.elevation_plot_items:
            each.remove()
            del each
        self.elevation_plot_items = []


    def drawElevationPlots(self):

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

    def removeAzimuthPlots(self):
        # Remove all plots
        for each in self.azimuth_plot_items:
            each.remove()
            del each
        self.azimuth_plot_items = []


    def drawAzimuthPlots(self):
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


    def removeWhiPlot(self):
        if self.whi_plot_item != None:
            self.whi_plot_item.remove()
            del self.whi_plot_item
        self.whi_plot_item = None


    def drawWhiPlot(self):
        
        #self.removeWhiPlot()
        
        self.whi_label.update()
        self.whi_label.setVisible(self.active_designated() and self.scene.whi_active and self.scene.radiating)

        if self.scene.whi_active and self.active_designated() and self.scene.radiating:

            if len(self.list_of_coords) > 1:
                whi_point = self.scene.getWhiPoint(self.list_of_coords[0])
                if whi_point:
                    x = whi_point.x()
                    y = whi_point.y()
                
                    self.whi_plot_item = WhiPlotItem(x, y, parent=None, scene=self.scene, parent_track=self)
        
                

    def clear(self):
        # Dumps all plots (coords) and de-designates the track
        if self.designated():
            self.toggleDesignated()
        
        self.list_of_coords = []        # Could this empty list be a problem???!!!!????


    def resetHistoryPlots(self):
        self.list_of_coords = self.list_of_coords[:1]

    def resetCallsign(self):
        self.callsign_string = ''


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
            
            