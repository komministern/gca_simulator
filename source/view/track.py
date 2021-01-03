#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    Copyright � 2016, 2017 Oscar Franz�n <oscarfranzen@yahoo.se>
#
#    This file is part of GCA Simulator.

from PySide2 import QtCore, QtWidgets, QtGui
import numpy as np
from .plot import CorrelatedPlotItem, HistoricPlotItem, WhiPlotItem, UnCorrelatedPlotItem, InvisiblePlotItem, UnCorrelatedTrackedPlotItem, CorrelatedTrackedPlotItem
from .label import ElevationLabel, AzimuthLabel, WhiLabel

class VisualTrack(QtCore.QObject):
    
    # max_historic_tracks = 15
    
    ELEVATION = 0
    AZIMUTH = 1
    
    
    def __init__(self, scene):
        super(VisualTrack, self).__init__()
        
        self.scene = scene
        
        # self.list_of_el_coords = []
        # self.list_of_az_coords = []
        # self.list_of_el_hits = []
        # self.list_of_az_hits = []
    
        #self.list_of_extrapolated_coords = []
        
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

        #self.inactive_due_to_no_updates = False

        #self.max_historic_az_plots = 0
        self.max_historic_plots = 0

        self.az_coordinate = None
        self.el_coordinate = None
        self.az_extrapolated = False
        self.el_extrapolated = False


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
            self.resetSize()
            
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
            self.resetSize()

        else:
            self.scene.designated_tracks.insert(0, self)
            self.setActive()
            self.draw(elevation=True, azimuth=True, whi=True)
            #self.drawWhiPlot()
            
            if len(self.scene.designated_tracks) > 1:
                self.scene.designated_tracks[1].setPassive()
                self.scene.designated_tracks[1].draw(elevation=True, azimuth=True, whi=True)
                #self.scene.designated_tracks[1].drawWhiPlot()
        
        # This signal is for updating the AC and LeaderDirection button windows
        #self.scene.active_designated_track_changed.emit()
    

    # def extrapolate(self, new_coord, historic_coord_list):
    #     if len(historic_coord_list) > 1:
            
    #         delta = historic_coord_list[0] - historic_coord_list[1]
    #         extrapolated_coord = historic_coord_list[0] + delta
    #         return extrapolated_coord

    #     else:

    #         return []



    #new_time_stamp, self.tracks[name]

    def update(self, new_time_stamp, track):
        # This method is executed only when a new plot is processed. It is guaranteed that coord is
        # a valid coordinate.
        
        #print coord

        #print self.list_of_el_coords
        #print self.list_of_el_hits

        #el_hit, az_hit = hits

        self.track = track

        # Update list of recorded hits for each antenna
        # The first two hit entries of the track will always be True

        # if len(self.list_of_el_hits) == (self.max_historic_tracks + 1):    # List for simulating missed targets in separate antennas
        #     del self.list_of_el_hits[-1]
        # if len(self.list_of_el_hits) < 2:
        #     el_hit = True
        # self.list_of_el_hits.insert(0, el_hit)

        # if len(self.list_of_az_hits) == (self.max_historic_tracks + 1):    # List for simulating missed targets in separate antennas
        #     del self.list_of_az_hits[-1]
        # if len(self.list_of_az_hits) < 2:
        #     az_hit = True
        # self.list_of_az_hits.insert(0, az_hit)


        # Update list of plot coordinates

        # if len(self.list_of_el_coords) == (self.max_historic_tracks + 1):
        #     del self.list_of_el_coords[-1]

        # if not el_hit:
        #     extrapolated_el_coord = self.extrapolate(coord, self.list_of_el_coords)
        #     self.list_of_el_coords.insert(0, extrapolated_el_coord)
        # else:
        #     self.list_of_el_coords.insert(0, coord)


        # if len(self.list_of_az_coords) == (self.max_historic_tracks + 1):
        #     del self.list_of_az_coords[-1]
        # if not az_hit:
        #     extrapolated_az_coord = self.extrapolate(coord, self.list_of_az_coords)
        #     self.list_of_az_coords.insert(0, extrapolated_az_coord)
        # else:
        #     self.list_of_az_coords.insert(0, coord)


        # Calculate the varius label values

        self.calculateDistanceToTd()
        #self.calculateVelocity()
        self.calculateAzimuthDeviation()

        if new_time_stamp == self.track.targets[0].time_stamp:
            if self.max_historic_plots < 15:
                self.max_historic_plots += 1





    def setActive(self):
        self.elevation_label.setActiveColors()
        self.azimuth_label.setActiveColors()
        self.elevation_label.setActiveZValue()
        self.azimuth_label.setActiveZValue()
        
        # This signal is for updating the AC and LeaderDirection button windows
        #self.scene.active_designated_track_changed.emit()
        
        
    def setPassive(self):
        self.elevation_label.setPassiveColors()
        self.azimuth_label.setPassiveColors()
        self.elevation_label.setPassiveZValue()
        self.azimuth_label.setPassiveZValue()




    # Structure the drawing of the tracks
    # Break out the remove plots as separate methods
    

    def el_label_visible(self):
        return True
        # if len(self.list_of_el_hits) > 2:
        #     return self.list_of_el_hits[0] or self.list_of_el_hits[1] or self.list_of_el_hits[2]
        # else:
        #     return False
        
    
    def az_label_visible(self):
        return True
        # if len(self.list_of_az_hits) > 2:
        #     return self.list_of_az_hits[0] or self.list_of_az_hits[1] or self.list_of_az_hits[2]
        # else:
        #     return False


    def draw(self, elevation=False, azimuth=False, whi=False, only_remove=False):
        
        #if len(self.list_of_el_coords) > 0:        # Do nothing if there are no plots to draw
        
        self.calculateElevationDeviation()          # This deviation is dependant on the glideslope!!! That is why it is executed here.
    
        self.elevation_label.update()
        self.azimuth_label.update()

        azimuth_point = self.scene.getAzimuthPoint(self.track.targets[0].az_coordinate)#  self.list_of_az_coords[0])
        az_y = azimuth_point.y()
        elevation_point = self.scene.getElevationPoint(self.track.targets[0].el_coordinate)#self.list_of_el_coords[0])
        el_y = elevation_point.y()

        # Make labels visible (or the opposite)
        self.elevation_label.setVisible(self.designated() and self.scene.radiating and self.el_label_visible() and elevation_point.y() > (self.scene.elevationgraphicsareatopleft_y + self.scene.plot_radius) and elevation_point.x() < self.scene.elevationgraphicsareabottomright_x)
        self.azimuth_label.setVisible(self.designated() and self.scene.radiating and self.az_label_visible() and azimuth_point.y() > (self.scene.azimuthgraphicsareatopleft_y + self.scene.plot_radius) and azimuth_point.y() < (self.scene.azimuthgraphicsareabottomright_y + self.scene.plot_radius) and azimuth_point.x() < self.scene.azimuthgraphicsareabottomright_x)
        self.whi_label.setVisible(self.active_designated() and self.scene.radiating)          # More work needed here!!!!!!!!!!!!

        # Remove the old plots
        if elevation:
            self.removeElevationPlots()
        if azimuth:
            self.removeAzimuthPlots()
        if whi:
            self.removeWhiPlot()

        # Draw the new plots
        if not only_remove and self.scene.radiating:        # Hmmmmmmm..............
            if elevation:
                self.drawElevationPlots()
            if azimuth:
                self.drawAzimuthPlots()
            if whi and self.active_designated():
                pass
                self.drawWhiPlot()
        
        
                
    
    def removeElevationPlots(self):
        # Remove all plots
        for each in self.elevation_plot_items:
            each.remove()
            del each
        self.elevation_plot_items = []


    def drawElevationPlots(self):

        historic_plots_drawn = 0

        # Draw new plots
        #for i in range(self.scene.nhist):

        for i in range(self.scene.nhist + 1):
            
            if i < len(self.track.targets):


        #for i in range(len(self.track.targets)):
            
            
            #if i < len(self.track.targets):# and historic_plots_drawn < self.scene.nhist:   # 1 + nhist
            
                # elevation_point = self.scene.getElevationPoint(self.list_of_el_coords[i])
                elevation_point = self.scene.getElevationPoint(self.track.historic_coordinate(i, 'el'))
                
                if elevation_point != None:     # This should not happen
                
                    x = elevation_point.x()
                    y = elevation_point.y()
            
                    if (x < (self.scene.graphicsareawidth - self.scene.plot_radius)) and (y > (self.scene.elevationgraphicsareatopleft_y + self.scene.plot_radius)):
                    # If this is a hit in reasonable x range, draw a visible plot
            
                        if i == 0:
                            # This is a ordinary plot
                            if self.track.targets[0].el_hit:
                                if self.track.targets[0].az_hit:
                                    self.elevation_plot_items.append(CorrelatedTrackedPlotItem(x, y, parent=None, scene=self.scene, parent_track=self))
                                else:
                                    self.elevation_plot_items.append(UnCorrelatedTrackedPlotItem(x, y, parent=None, scene=self.scene, parent_track=self))
                            # else:
                            #     self.elevation_plot_items.append(InvisiblePlotItem(x, y, parent=None, scene=self.scene, parent_track=self))


                        elif self.scene.hist_active and (historic_plots_drawn < self.max_historic_plots):
                            # This is a historic plot
                            if self.track.targets[i].el_hit:
                                self.elevation_plot_items.append(HistoricPlotItem(x, y, parent=None, scene=self.scene, parent_track=self))
                                historic_plots_drawn += 1
                            # else:
                            #     self.elevation_plot_items.append(InvisiblePlotItem(x, y, parent=None, scene=self.scene, parent_track=self))

        

                # else:

                #     print('ERROR drawing El plot (coordinate is None)')


    def removeAzimuthPlots(self):
        # Remove all plots
        for each in self.azimuth_plot_items:
            each.remove()
            del each
        self.azimuth_plot_items = []


    def drawAzimuthPlots(self):
        # Draw new plots

        historic_plots_drawn = 0

        for i in range(self.scene.nhist + 1):
            
            if i < len(self.track.targets):   # 1 + nhist

        # for i in range(len(self.list_of_az_coords)):
            
        #     if i <= self.scene.nhist:   # 1 + nhist
            
                azimuth_point = self.scene.getAzimuthPoint(self.track.targets[i].az_coordinate)# list_of_az_coords[i])
                
                if azimuth_point != None:
                
                    x = azimuth_point.x()
                    y = azimuth_point.y()
            
                    if (x < (self.scene.graphicsareawidth - self.scene.plot_radius)) and (y > (self.scene.azimuthgraphicsareatopleft_y + self.scene.plot_radius)) and (y < (self.scene.azimuthgraphicsareabottomright_y + self.scene.plot_radius)):
                    #if self.list_of_az_hits[i] and (x < (self.scene.graphicsareawidth - self.scene.plot_radius)) and (y > (self.scene.azimuthgraphicsareatopleft_y + self.scene.plot_radius)) and (y < (self.scene.azimuthgraphicsareabottomright_y + self.scene.plot_radius)):
                    # If this is a hit in reasonable x range, AND in reasonable y range, draw a visible plot
            
                        #if i == 0:
                        #    # This is a ordinary plot
                        #    self.azimuth_plot_items.append(CorrelatedPlotItem(x, y, parent=None, scene=self.scene, parent_track=self))
                        #elif (i > 0) and self.scene.hist_active:
                        #    # This is a historic plot
                        #    self.azimuth_plot_items.append(HistoricPlotItem(x, y, parent=None, scene=self.scene, parent_track=self))

                        if i == 0:
                            # This is a ordinary plot
                            #if self.list_of_az_hits[0]:
                            if self.track.targets[0].az_hit:
                                if self.track.targets[0].el_hit:
                                    self.azimuth_plot_items.append(CorrelatedTrackedPlotItem(x, y, parent=None, scene=self.scene, parent_track=self))
                                else:
                                    self.azimuth_plot_items.append(UnCorrelatedTrackedPlotItem(x, y, parent=None, scene=self.scene, parent_track=self))
                            # else:
                            #     self.azimuth_plot_items.append(InvisiblePlotItem(x, y, parent=None, scene=self.scene, parent_track=self))


                        elif self.scene.hist_active and historic_plots_drawn < self.max_historic_plots:
                            # This is a historic plot
                            if self.track.targets[i].az_hit:
                                self.azimuth_plot_items.append(HistoricPlotItem(x, y, parent=None, scene=self.scene, parent_track=self))
                                historic_plots_drawn += 1
                            # else:
                            #     self.azimuth_plot_items.append(InvisiblePlotItem(x, y, parent=None, scene=self.scene, parent_track=self))




    def removeWhiPlot(self):
        if self.whi_plot_item != None:
            self.whi_plot_item.remove()
            del self.whi_plot_item
        self.whi_plot_item = None


    def drawWhiPlot(self):

        #self.removeWhiPlot()
        
        self.whi_label.update()
        self.whi_label.setVisible(self.active_designated() and self.scene.whi_active and self.scene.radiating)

        if self.scene.whi_active and self.active_designated() and self.scene.radiating:# and self.track.targets[0].az_hit and self.track.targets[0].el_hit:

            #if len(self.list_of_el_coords) > 1:
            whi_point = self.scene.getWhiPoint(self.track.targets[0].el_coordinate)
            if whi_point:
                x = whi_point.x()
                y = whi_point.y()
            
                if self.track.targets[0].az_hit and self.track.targets[0].el_hit:

                    self.whi_plot_item = WhiPlotItem(x, y, parent=None, scene=self.scene, parent_track=self, visible=True)

                #elif self.track.targets[0].az_hit or self.track.targets[0].el_hit:

                #    self.whi_plot_item = WhiPlotItem(x, y, parent=None, scene=self.scene, parent_track=self, visible=True)
                    # This is an opportunity to show uncorrelated plots in a different way (perhaps in yellow color?) instead of
                    # just blanking the whi plot. What happens IRL?
        
    def destroy(self):

        # Make sure we are not designated
        if self.designated():
            self.toggleDesignated()

        # Un-draw all the plots (remove the items)
        self.draw(elevation=True, azimuth=True, whi=True, only_remove=True)

        # Remove this object from


    #def clear(self):
        # Dumps all plots (coords) and de-designates the track
    #    if self.designated():
    #        self.toggleDesignated()
        
    #    self.list_of_coords = []        # Could this empty list be a problem???!!!!????


    def resetHistoryPlots(self):

        #self.scene.max_available_historic_tracks = 0

        self.max_historic_plots = 0

        
        #self.list_of_el_coords = self.list_of_el_coords[:2]     # If :1 it generates occational faults!!!!!!!!!!!!! Hmmmm......
        #self.list_of_az_coords = self.list_of_az_coords[:2]
        #self.list_of_el_coords = self.list_of_el_coords[:1]
        #self.list_of_az_coords = self.list_of_az_coords[:1]

    def resetCallsign(self):
        self.callsign_string = ''

    def resetSize(self):
        self.size_string = 'M'


    def calculateDistanceToTd(self):    # Let's do this calculation based on the el coords

        meters = np.linalg.norm(self.track.targets[0].el_coordinate)
        nautical_miles = meters / 1852.0
        self.distance_to_td = nautical_miles

        # if len(self.list_of_el_coords) > 0:
        #     meters = np.linalg.norm(self.list_of_el_coords[0])
        #     nautical_miles = meters / 1852.0
        #     self.distance_to_td = nautical_miles

            

    # def calculateVelocity(self):
    #     if len(self.list_of_el_coords) >= 2:
            
    #         if len(self.list_of_el_coords[0]) == 3 and len(self.list_of_el_coords[1]) == 3:
                
    #             meters_per_second = np.linalg.norm(self.list_of_el_coords[1] - self.list_of_el_coords[0]) / self.scene.delta_t
    #             knots = meters_per_second * 1.943844 
    #             self.velocity = knots
    #         else:
    #             self.velocity = 0.0


    def calculateElevationDeviation(self):
        
        plot_x = self.track.historic_coordinate(0, 'el')[0]
        plot_z = self.track.historic_coordinate(0, 'el')[2]

        preferred_height_in_m = -1.0 * plot_x * np.tan(self.scene.glideslope * np.pi / 180.0)
        deviation_from_glideslope_in_m = plot_z - preferred_height_in_m
        deviation_from_glideslope_in_feet = deviation_from_glideslope_in_m * 3.28084
        self.elevation_deviation = deviation_from_glideslope_in_feet

        

        # if len(self.list_of_el_coords) > 0:
        #     plot_x = self.list_of_el_coords[0][0]
        #     plot_z = self.list_of_el_coords[0][2]
        #     preferred_height_in_m = -1.0 * plot_x * np.tan(self.scene.glideslope * np.pi / 180.0)
        #     deviation_from_glideslope_in_m = plot_z - preferred_height_in_m
        #     deviation_from_glideslope_in_feet = deviation_from_glideslope_in_m * 3.28084
        #     self.elevation_deviation = deviation_from_glideslope_in_feet
        

    def calculateAzimuthDeviation(self):

        plot_y = self.track.historic_coordinate(0, 'az')[1]

        deviation_from_groundline_in_m = -1.0 * plot_y
        deviation_from_groundline_in_feet = deviation_from_groundline_in_m * 3.28084
        self.azimuth_deviation = deviation_from_groundline_in_feet

        # if len(self.list_of_az_coords) > 0:
        #     plot_y = self.list_of_az_coords[0][1]

        #     deviation_from_groundline_in_m = -1.0 * plot_y
        #     deviation_from_groundline_in_feet = deviation_from_groundline_in_m * 3.28084
        #     self.azimuth_deviation = deviation_from_groundline_in_feet
            
            