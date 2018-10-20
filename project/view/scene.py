#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    Copyright � 2016, 2017 Oscar Franz�n <oscarfranzen@yahoo.se>
#
#    This file is part of GCA Simulator.

from PySide import QtGui, QtCore
import numpy as np
import time

from track import Track

from coverage import ElevationCoverage, AzimuthCoverage
from glideslope import GlideSlope
from decisionheight import DecisionHeight
from runway import ElevationRunway, AzimuthRunway
from textinfo import TextInfo
from gca import ElevationGCA, AzimuthGCA
from axis import ElevationAxis, AzimuthAxis, RangeAxis, WHIAxis
from alerts import AlertsField
from mapsymbols import MapSymbols


class MyScene(QtGui.QGraphicsScene):

    scenetotaltopleft_x = 0.0
    scenetotaltopleft_y = 0.0
    scenetotalwidth = 1920.0 - 4.0
    scenetotalheight = 1080.0 - 4.0

    buttonwindowareawidth = 320.0
    buttonwindowareaheight = scenetotalheight

    buttonwindowareatopleft_x = scenetotalwidth - buttonwindowareawidth
    buttonwindowareatopleft_y = scenetotaltopleft_y

    # **** AREAS

    graphicsareawidth = scenetotalwidth - buttonwindowareawidth
    graphicsareaheight = scenetotalheight

    textgraphicsareawidth = graphicsareawidth
    textgraphicsareaheight = 60.0  # Absolute

    elevationgraphicsareawidth = graphicsareawidth
    elevationgraphicsareaheight = (graphicsareaheight - textgraphicsareaheight) / 2

    azimuthgraphicsareawidth = graphicsareawidth
    azimuthgraphicsareaheight = (graphicsareaheight - textgraphicsareaheight) / 2

    elevationgraphicsareatopleft_x = scenetotaltopleft_x
    elevationgraphicsareatopleft_y = scenetotaltopleft_y
    elevationgraphicsareabottomright_x = elevationgraphicsareatopleft_x + elevationgraphicsareawidth
    elevationgraphicsareabottomright_y = elevationgraphicsareatopleft_y + elevationgraphicsareaheight

    textgraphicsareatopleft_x = scenetotaltopleft_x
    textgraphicsareatopleft_y = elevationgraphicsareaheight
    textgraphicsareabottomright_x = textgraphicsareatopleft_x + textgraphicsareawidth
    textgraphicsareabottomright_y = textgraphicsareatopleft_y + textgraphicsareaheight

    azimuthgraphicsareatopleft_x = scenetotaltopleft_x
    azimuthgraphicsareatopleft_y = elevationgraphicsareaheight + textgraphicsareaheight
    azimuthgraphicsareabottomright_x = azimuthgraphicsareatopleft_x + azimuthgraphicsareawidth
    azimuthgraphicsareabottomright_y = elevationgraphicsareaheight + azimuthgraphicsareaheight + textgraphicsareaheight

    # **** WHI AXIS

    whiaxislength_x = scenetotalheight / 5
    whiaxislength_y = whiaxislength_x
    whiaxiszero_x = whiaxislength_x * 1.1
    whiaxiszero_y = whiaxislength_y * 0.7
    whiaxismarkinglength = 10.0

    # **** ELEVATION RANGE AXIS

    rangeaxiszero_x = 110.0    # Absolute position for x=0
    rangeaxismax_x = graphicsareawidth # Position for x=maxscale

    elevationrangeaxiszero_x = rangeaxiszero_x
    elevationrangeaxismax_x = rangeaxismax_x
    elevationrangeaxis_y = 8.0 / 9.0 * elevationgraphicsareaheight + elevationgraphicsareatopleft_y

    elevationminrangegraphicsrange = elevationrangeaxiszero_x / 4.0

    # **** AZIMUTH RANGE AXIS

    azimuthrangeaxiszero_x = rangeaxiszero_x
    azimuthrangeaxismax_x = rangeaxismax_x
    azimuthrangeaxis_y = azimuthgraphicsareaheight / 2 + azimuthgraphicsareatopleft_y

    axismarkinglength = 16.0    # Absolute value

    glideslopemarkinglength = axismarkinglength - 2.0
    
    azimuthminrangegraphicsrange = elevationminrangegraphicsrange

    # **** ELEVATION AXIS

    elevationaxis_x = rangeaxiszero_x * 0.6
    elevationaxismin_y = elevationgraphicsareabottomright_y
    elevationaxismax_y = elevationgraphicsareatopleft_y
    elevationaxiszero_y = elevationrangeaxis_y

    # **** AZIMUTH AXIS

    azimuthaxis_x = rangeaxiszero_x * 0.6
    azimuthaxismin_y = azimuthgraphicsareabottomright_y
    azimuthaxismax_y = azimuthgraphicsareatopleft_y
    azimuthaxiszero_y = azimuthrangeaxis_y

    # **** DECISIONHEIGHT LINE

    decisionheight_length = 150.0

    # **** PLOT SIZE
    
    plot_radius = 4.0
    
    # **** LABEL
    
    #label_displacement_x = 100.0
    #label_displacement_y = 100.0
    label_text_distance_x = 8.0
    label_leader_distance = 5.0
    label_standard_x_offset_magnitude = 150.0
    label_standard_y_offset_magnitude = 150.0
    
    # **** LEADER
    leader_initial_length = 150.0
    
    # **** ALERT FIELD
    
    alerts_field_width = 300.0
    alerts_field_centre_x = graphicsareawidth * 0.55
    alerts_field_top_y = 40.0
    alerts_frame_margin = 10.0

    # **** SIGNALS
    
    sound_alarm_on = QtCore.Signal()
    sound_alarm_off = QtCore.Signal()
    
    active_designated_track_changed = QtCore.Signal()
    mti_lost = QtCore.Signal()


    def __init__(self):
        super(MyScene, self).__init__()
        self.setBackgroundBrush(QtCore.Qt.black)


        # Pens, brushes and colors
        self.button_window_brush = QtGui.QBrush(QtCore.Qt.darkBlue)
        
        self.axis_font = QtGui.QFont("Helvetica", 10)
        self.axis_color = QtGui.QColor(255, 165, 0, 255)
        
        self.axis_pen = QtGui.QPen(self.axis_color)
        self.axis_pen.setWidth(2.0)

        self.runway_color = QtCore.Qt.darkCyan
        self.runway_pen = QtGui.QPen(self.runway_color)
        self.runway_pen.setWidth(2)
        
        self.runway_font = QtGui.QFont(self.axis_font)
        self.runway_brush = QtGui.QBrush(self.runway_color)
        
        self.glideslope_color = QtGui.QColor(60, 179, 113, 255)
        self.glideslope_pen = QtGui.QPen(self.glideslope_color)
        self.glideslope_pen.setWidth(2)
        
        self.decisionheight_pen = self.glideslope_pen
        
        self.gca_color = QtGui.QColor(139,0,139,255)
        self.gca_brush = QtGui.QBrush(self.gca_color)
        
        self.coverage_pen = QtGui.QPen(self.gca_color)
        self.coverage_pen.setStyle(QtCore.Qt.DashLine)
        
        self.az_ant_elevation_pen = QtGui.QPen(self.coverage_pen)
        
        self.textinfo_color = self.glideslope_color
        self.textinfo_font = QtGui.QFont(self.axis_font)
        self.textinfo_brush = QtGui.QBrush(self.textinfo_color)
        
        self.plot_brush = QtGui.QBrush(QtCore.Qt.white)
        self.plot_pen = QtGui.QPen(QtCore.Qt.white)

        self.uncorrelated_plot_brush = QtGui.QBrush(QtCore.Qt.yellow)
        self.uncorrelated_plot_pen = QtGui.QPen(QtCore.Qt.yellow)
        
        self.historic_plot_brush = QtGui.QBrush(QtCore.Qt.darkGray)
        self.historic_plot_pen = QtGui.QPen(QtCore.Qt.darkGray)

        self.active_label_color = QtCore.Qt.yellow
        self.passive_label_color = QtGui.QColor(102,178,255,255)
        
        self.active_label_pen = QtGui.QPen(self.active_label_color)
        self.active_label_pen.setWidth(2)
        self.active_label_brush = QtGui.QBrush(self.active_label_color)
        self.active_label_font = QtGui.QFont("Helvetica", 10)
        self.active_label_font.setBold(True)
        
        self.passive_label_pen = QtGui.QPen(self.passive_label_color)
        self.passive_label_pen.setWidth(2)
        self.passive_label_brush = QtGui.QBrush(self.passive_label_color)
        self.passive_label_font = QtGui.QFont("Helvetica", 10)
        self.passive_label_font.setBold(True)
        
        self.active_leader_pen = QtGui.QPen(self.active_label_color)
        self.passive_leader_pen = QtGui.QPen(self.passive_label_color)
        
        self.alerts_color = self.textinfo_color
        self.alerts_font = QtGui.QFont("Helvetica", 10)
        self.alerts_field_pen = QtGui.QPen(self.alerts_color)
        self.alerts_field_pen.setWidth(2)
        self.alerts_brush = QtGui.QBrush(self.alerts_color)
        

        # Attributes ('global') relevant for the display
        self.rangescale = None
        self.elevationscale = None
        self.azimuthscale = None
        self.glideslope = None
        self.azantelev = None
        self.nhist = None
        self.elantazim = None

        self.decisionheight = 0         # This one is set here due to no button can set it to zero.
        
        self.active_airport = None
        self.active_runway = None
        
        self.wx_active = False
        self.obs_active = False
        self.map_active = False
        self.whi_active = False
        self.hist_active = False
        self.radarcover_active = False
        self.synvid_active = False
        
        self.line_1_visible = False
        self.line_2_visible = False
        self.line_3_visible = False
        self.leader_visible = False


        # States
        self.radiating = False
        self.connected = False
        

        # Windows related stuff
        self.movablewindowZval = 20.0
        self.activewindowtopborders = []


        # Coordinates
        #self.airplane_coordinate = np.array([])
        self.thr_coordinate = np.array([])
        self.eor_coordinate = np.array([])
        self.gca_coordinate = np.array([])
        #self.mti_1_coordinate = np.array([])
        #self.mti_2_coordinate = np.array([])
        
        # Hits
        #self.airplane_hit = (False, False)
        #self.mti_1_hit = (False, False)
        #self.mti_2_hit = (False, False)


        # Points
        self.touchdown_elevation_point = None
        self.touchdown_azimuth_point = None
        self.airplane_elevation_point = None
        self.airplane_azimuth_point = None
        self.threshold_elevation_point = None
        self.threshold_azimuth_point = None
        self.eor_elevation_point = None
        self.eor_azimuth_point = None
        self.gca_elevation_point = None
        self.gca_azimuth_point = None
        #self.mti_1_elevation_point = None
        #self.mti_1_azimuth_point = None
        #self.mti_2_elevation_point = None
        #self.mti_2_azimuth_point = None



        # Z Values
        self.axis_zvalue = 0.6
        self.textinfo_zvalue = 0.0
        self.alerts_zvalue = 1.0
        self.runway_zvalue = 3.0
        self.gca_zvalue = 2.5
        self.coverage_zvalue = 0.4
        self.az_ant_elevation_zvalue = self.coverage_zvalue
        self.glideslope_zvalue = 2.0
        self.historic_plot_zvalue = 5.0
        self.plot_zvalue = 10.0
        self.active_label_zvalue = 8.0
        self.active_leader_zvalue = 8.0
        self.passive_label_zvalue = 7.0
        self.passive_leader_zvalue = 7.0
        self.decisionheight_zvalue = 0.5
        self.button_window_zvalue = self.plot_zvalue + 1.0
        self.mapsymbols_zvalue = 0.6


        # Initialize the button window part of the scene
        self.setSceneRect(0.0, 0.0, self.scenetotalwidth, self.scenetotalheight)
        self.button_window_rect = QtGui.QGraphicsRectItem(self.buttonwindowareatopleft_x, self.buttonwindowareatopleft_y, self.buttonwindowareawidth, self.buttonwindowareaheight)
        self.button_window_rect.setBrush(self.button_window_brush)
        self.button_window_rect.setZValue(self.button_window_zvalue)
        self.addItem(self.button_window_rect)


        # Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.drawTextInfo)
        self.timer.start(1000)

        self.current_time_stamp = 0.0
        self.previous_time_stamp = 0.0
        self.delta_t = 0.0


        # Tracks
        self.tracks = {}
        #self.airplane_track = Track(self)
        #self.mti_1_track = Track(self)
        #self.mti_2_track = Track(self)
        
        #self.tracks = [self.airplane_track, self.mti_1_track, self.mti_2_track]
        self.designated_tracks = []
        


        # Items
        self.elevation_coverage_item = ElevationCoverage(self)
        self.azimuth_coverage_item = AzimuthCoverage(self)
        self.glideslope_item = GlideSlope(self)
        
        self.decisionheight_item = DecisionHeight(self)
        
        self.elevation_runway_item = ElevationRunway(self)
        self.azimuth_runway_item = AzimuthRunway(self)
        
        self.textinfo_item = TextInfo(self)
        
        self.elevation_gca_item = ElevationGCA(self)
        self.azimuth_gca_item = AzimuthGCA(self)
        
        self.elevation_axis_item = ElevationAxis(self)
        self.azimuth_axis_item = AzimuthAxis(self)
        
        self.range_axis_item = RangeAxis(self)
        
        self.whi_axis_item = WHIAxis(self)
        
        self.alerts_field = AlertsField(self)

        self.mapsymbols_item = MapSymbols(self)
        



    # METHODS


    def selectAsFirstDesignatedTarget(self, track):     # Also see exchangeWhiTrack in presenter......
        
        first_track = self.designated_tracks[0]
        
        if track != first_track:                # This ensures that len(designated_tracks) > 1
            self.designated_tracks.remove(track)
            self.designated_tracks.insert(0, track)

            self.designated_tracks[1].setPassive()
            self.designated_tracks[1].draw(elevation=True, azimuth=True, whi=True)
        
            self.designated_tracks[0].setActive()
            self.designated_tracks[0].draw(elevation=True, azimuth=True, whi=True)


    #def processReceivedPlot(self, airplane_coordinate, threshold_coordinate, eor_coordinate, gca_coordinate, mti_1_coordinate, mti_2_coordinate, new_time_stamp, airplane_hit, mti_1_hit, mti_2_hit):

        #self.previous_time_stamp = self.current_time_stamp
        #self.current_time_stamp = new_time_stamp
        #self.delta_t = self.current_time_stamp - self.previous_time_stamp


        #self.airplane_coordinate = airplane_coordinate
        #self.threshold_coordinate = threshold_coordinate
        #self.eor_coordinate = eor_coordinate
        #self.gca_coordinate = gca_coordinate
        #self.mti_1_coordinate = mti_1_coordinate
        #self.mti_2_coordinate = mti_2_coordinate
        #self.airplane_hit = airplane_hit
        #self.mti_1_hit = mti_1_hit
        #self.mti_2_hit = mti_2_hit

        #self.updateAllTracks()

        #self.drawElevationGraphics()
        #self.drawAzimuthGraphics()
        
        #self.drawWhiPlot()

        #self.drawTextInfo()




    def processReceivedPlots(self, new_time_stamp, thr_coordinate, eor_coordinate, gca_coordinate, aircraft_coordinates, aircraft_hits):

        self.previous_time_stamp = self.current_time_stamp
        self.current_time_stamp = new_time_stamp

        self.delta_t = self.current_time_stamp - self.previous_time_stamp


        self.aircraft_coordinates = aircraft_coordinates
        self.thr_coordinate = thr_coordinate
        self.eor_coordinate = eor_coordinate
        self.gca_coordinate = gca_coordinate

        self.aircraft_hits = aircraft_hits

        self.updateAllTracks()

        self.drawElevationGraphics()
        self.drawAzimuthGraphics()
        
        self.drawWhiPlot()

        self.drawTextInfo()


    def resetAllHistoryPlots(self):
        for track_name in self.tracks:
            self.tracks[track_name].resetHistoryPlots()

    def drawAllElevationTracks(self):
        for track_name in self.tracks:
            self.tracks[track_name].draw(elevation=True, azimuth=False)

    def drawAllAzimuthTracks(self):
        for track_name in self.tracks:
            self.tracks[track_name].draw(elevation=False, azimuth=True)
    
    def removeAllTracks(self):
        for track_name in self.tracks:
            self.tracks[track_name].destroy()
        self.tracks = {}
        #self.tracks[track_name].draw(elevation=True, azimuth=True, whi=True, only_remove=True)

    def drawAllTracks(self):
        for track_name in self.tracks:
            self.tracks[track_name].draw(elevation=True, azimuth=True, whi=True)

    #def clearAllTracks(self):
        #self.tracks = {}
        #self.removeAllTracks()
        
    #    for track_name in self.tracks:
    #        self.tracks[track_name].clear()
    #        self.tracks[track_name].resetCallsign()
        
    #    self.tracks = {}
        

    def updateAllTracks(self):
        
        print self.tracks

        if 'mti' in self.tracks:
            if (not True in self.tracks['mti'].list_of_el_hits[0:3]) or (not True in self.tracks['mti'].list_of_az_hits[0:3]):
                self.mti_lost.emit()
                #print 'lost mti'

        tracks_to_be_removed = []
        for track_name in self.tracks:
            s = set(self.tracks[track_name].list_of_el_hits[0:3]) | set(self.tracks[track_name].list_of_az_hits[0:3])   # union 
            if len(s) == 1 and (False in s):
                tracks_to_be_removed.append(track_name)


        for track_name in tracks_to_be_removed:
            self.tracks[track_name].destroy()
            del self.tracks[track_name]

        for track_name in self.aircraft_coordinates:
            (el_hit, az_hit) = self.aircraft_hits[track_name]
            if not track_name in self.tracks and (el_hit or az_hit):
                self.tracks[track_name] = Track(self)
            
        for track_name in self.tracks:
            self.tracks[track_name].update(self.aircraft_coordinates[track_name], self.aircraft_hits[track_name])



    def drawWhiPlot(self):                              # Noooooooooooooooooooooooooooooooooooooooo!!!!!!! Should be inside Track!!!!!!!!!!!!!!!!!
        if len(self.designated_tracks) > 0:
            self.designated_tracks[0].draw(elevation=False, azimuth=False, whi=True)


    def drawAllGraphics(self):
        self.drawElevationGraphics()
        self.drawAzimuthGraphics()


    def drawElevationGraphics(self):
        # Calculate all points (except for the track points, which are calculated in the drawElevationTrack method)
        self.touchdown_elevation_point = self.getElevationPoint(np.array([0.0, 0.0, 0.0]))
        self.threshold_elevation_point = self.getElevationPoint(self.thr_coordinate)
        self.eor_elevation_point = self.getElevationPoint(self.eor_coordinate)
        self.gca_elevation_point = self.getElevationPoint(self.gca_coordinate)
        #self.mti_1_elevation_point = self.getElevationPoint(self.mti_1_coordinate)
        #self.mti_2_elevation_point = self.getElevationPoint(self.mti_2_coordinate)

        self.drawElevationRunway()
        self.drawGlideSlope()
        self.drawDecisionHeight()
        self.drawElevationGCA()
        self.drawElevationCoverage()
        self.drawAllElevationTracks()

    def drawAzimuthGraphics(self):
        # Calculate all points (except for the track points, which are calculated in the drawAzimuthTrack method)
        self.touchdown_azimuth_point = self.getAzimuthPoint(np.array([0.0, 0.0, 0.0]))
        self.threshold_azimuth_point = self.getAzimuthPoint(self.thr_coordinate)
        self.eor_azimuth_point = self.getAzimuthPoint(self.eor_coordinate)
        self.gca_azimuth_point = self.getAzimuthPoint(self.gca_coordinate)
        #self.mti_1_azimuth_point = self.getAzimuthPoint(self.mti_1_coordinate)
        #self.mti_2_azimuth_point = self.getAzimuthPoint(self.mti_2_coordinate)
        
        self.drawAzimuthRunway()
        self.drawAzimuthGCA()
        self.drawAzimuthCoverage()
        self.drawAllAzimuthTracks()

    def drawElevationCoverage(self):
        self.elevation_coverage_item.draw()
        
    def drawAzimuthCoverage(self):
        self.azimuth_coverage_item.draw()

    def drawGlideSlope(self):
        self.glideslope_item.draw()
        
    def drawDecisionHeight(self):
        self.decisionheight_item.draw()

    def drawElevationRunway(self):
        self.elevation_runway_item.draw()
        
    def drawAzimuthRunway(self):
        self.azimuth_runway_item.draw()

    def drawTextInfo(self):
        self.textinfo_item.draw()

    def drawElevationGCA(self):
        self.elevation_gca_item.draw()
        
    def drawAzimuthGCA(self):
        self.azimuth_gca_item.draw()

    def drawElevationAxis(self):
        self.elevation_axis_item.draw()
        
    def drawAzimuthAxis(self):
        self.azimuth_axis_item.draw()

    def drawRangeAxis(self):
        self.range_axis_item.draw()

    def drawWhiAxis(self):
        self.whi_axis_item.draw()

    def drawMapSymbols(self):
        
        if self.mapsymbols_item:
            self.removeItem(self.mapsymbols_item)
            del self.mapsymbols_item
            self.mapsymbols_item = None
            
        if self.map_active:
            
            self.mapsymbols_item = QtGui.QGraphicsItemGroup(parent=None, scene=self)
            
            lineitem = QtGui.QGraphicsLineItem(0.0, 0.0, 100.0, 100.0, parent=self.mapsymbols_item)
            lineitem.setPen(self.axis_pen)
            
            



    # Coordinate transformations

    def getElevationPoint(self, np_coord):
        if len(np_coord) == 3 and (self.elevationscale != None):
            
            range_m = np_coord[0]
            altitude_m = np_coord[2]
            azimuth_m = np_coord[1]

            range_x_pixel = self.range_to_scenexcoord(range_m)
            altitude_y_pixel = self.altitude_to_sceneycoord(altitude_m)
            #azimuth_y_pixel = self.azimuth_to_sceneycoord(azimuth_m)

            elev_point = QtCore.QPointF(range_x_pixel, altitude_y_pixel)
            #azim_point = QtCore.QPointF(range_x_pixel, azimuth_y_pixel)

            return elev_point
        else:
            return None
        
    def getAzimuthPoint(self, np_coord):
        if len(np_coord) == 3 and (self.azimuthscale != None):
            
            range_m = np_coord[0]
            altitude_m = np_coord[2]
            azimuth_m = np_coord[1]

            range_x_pixel = self.range_to_scenexcoord(range_m)
            #altitude_y_pixel = self.altitude_to_sceneycoord(altitude_m)
            azimuth_y_pixel = self.azimuth_to_sceneycoord(azimuth_m)

            #elev_point = QtCore.QPointF(range_x_pixel, altitude_y_pixel)
            azim_point = QtCore.QPointF(range_x_pixel, azimuth_y_pixel)

            return azim_point
        else:
            return None


    def getWhiPoint(self, np_coord):
        if len(np_coord) == 3 and (self.glideslope != None):

            range_m = np_coord[0]
            altitude_m = np_coord[2]
            azimuth_m = np_coord[1]

            whi_azimuth_ft = azimuth_m * 3.2808399
            #print 'real altitude m  ' + str(altitude_m)

            ideal_altitude_m = range_m * np.tan(self.glideslope * np.pi / 180.0)
            #print 'ideal altitude m  ' + str(ideal_altitude_m)
            whi_altitude_ft = (altitude_m + ideal_altitude_m) * 3.2808399
            #print 'whi altitude m  ' + str(whi_altitude_ft / 3.2808399)
            #print ''

            if np.absolute(whi_azimuth_ft) < 1000.0 and np.absolute(whi_altitude_ft) < 500.0:

                whi_x_pixel = -(whi_azimuth_ft / 1000.0) * self.whiaxislength_x / 2.0 + self.whiaxiszero_x
                whi_y_pixel = -(whi_altitude_ft / 500.0) * self.whiaxislength_y / 2.0 + self.whiaxiszero_y
                return QtCore.QPointF(whi_x_pixel, whi_y_pixel)
            else:
                return None
        else:
            return None


    def range_to_scenexcoord(self, range_m):
        # input in m
        # 1 nmi is 1852 m

        #   range_nmi   scene
        #   0.0         rangeaxiszero_x
        #   max         rangeaxixmax_x
        range_nmi = -1.0 * range_m / 1852.0
        nmi_per_pixel = self.rangescale / (self.rangeaxismax_x - self.rangeaxiszero_x)
        return self.rangeaxiszero_x + range_nmi / nmi_per_pixel

    def altitude_to_sceneycoord(self, altitude_m):
        # input in m
        # 1 m is 3.2808399 ft

        #   range_ft    scene
        #   0.0         elevationaxiszero_y
        #   max         elevationaxismax_y
        altitude_ft = 3.2808399 * altitude_m
        ft_per_pixel = self.elevationscale / (self.elevationaxismax_y - self.elevationaxiszero_y)
        return self.elevationaxiszero_y + altitude_ft / ft_per_pixel

    def azimuth_to_sceneycoord(self, azimuth_m):
        # input in m
        # 1 m is 3.2808399 ft

        #   range_ft    scene
        #   0.0         azimuthaxiszero_y
        #   max         azimuthaxismax_y
        #   min         azimuthaxismin_y
        azimuth_ft = 3.2808399 * azimuth_m
        ft_per_pixel = self.azimuthscale / (self.azimuthaxiszero_y - self.azimuthaxismax_y)
        return self.azimuthaxiszero_y + azimuth_ft / ft_per_pixel


    # WINDOW RELATED METHODS

    def registerWindowTopBorder(self, windowtopborder):
        self.activewindowtopborders.append(windowtopborder)

    def unFocusAllWindowTopBorders(self):
        if len(self.activewindowtopborders) > 0:
            for each in self.activewindowtopborders:
                each.setUnFocused()

    def getNewZVal(self):
        self.movablewindowZval += 0.001
        return self.movablewindowZval
