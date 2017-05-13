#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    Copyright © 2016, 2017 Oscar Franzén <oscarfranzen@yahoo.se>
#
#    This file is part of GCA Simulator.

from PySide import QtGui, QtCore
import numpy as np
import time

class MyScene(QtGui.QGraphicsScene):

    scenetotaltopleft_x = 0.0
    scenetotaltopleft_y = 0.0
    scenetotalwidth = 1600.0
    scenetotalheight = 1200.0

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

    # **** ELEVATION RANGE AXIS

    rangeaxiszero_x = 110.0    # Absolute position for x=0
    rangeaxismax_x = graphicsareawidth # Position for x=maxscale

    elevationrangeaxiszero_x = rangeaxiszero_x
    elevationrangeaxismax_x = rangeaxismax_x
    elevationrangeaxis_y = 8.0 / 9.0 * elevationgraphicsareaheight + elevationgraphicsareatopleft_y

    elevationminrangegraphicsrange = elevationrangeaxiszero_x / 3.0

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


    def __init__(self):
        super(MyScene, self).__init__()
        self.setSceneRect(0.0, 0.0, self.scenetotalwidth, self.scenetotalheight)
        self.addRect(self.buttonwindowareatopleft_x, self.buttonwindowareatopleft_y, self.buttonwindowareawidth, self.buttonwindowareaheight, brush=QtGui.QBrush(QtCore.Qt.darkBlue))
        self.setBackgroundBrush(QtCore.Qt.black)

        # Pens, brushes and colors
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
        
        self.gca_color = QtGui.QColor(139,0,139,255)
        self.gca_brush = QtGui.QBrush(self.gca_color)
        
        self.coverage_pen = QtGui.QPen(self.gca_color)
        self.coverage_pen.setStyle(QtCore.Qt.DashLine)
        
        self.az_ant_elevation_pen = QtGui.QPen(self.coverage_pen)
        
        self.textinfo_font = QtGui.QFont(self.axis_font)
        self.textinfo_brush = QtGui.QBrush(self.glideslope_color)
        

        # Attributes relevant for the display
        self.rangescale = None
        self.elevationscale = None
        self.azimuthscale = None
        self.glideslope = None
        self.azantelev = None
        
        self.active_airport = None
        self.active_runway = None
        
        self.wx_active = False
        self.obs_active = False
        self.map_active = False
        self.whi_active = False
        self.hist_active = False
        self.radarcover_active = False
        self.synvid_active = False
        
        

        # Windows related stuff
        self.movablewindowZval = 0.0
        self.activewindowtopborders = []
        
        # Coordinates
        self.airplane_coordinate = np.array([])
        self.threshold_coordinate = np.array([])
        self.eor_coordinate = np.array([])
        self.gca_coordinate = np.array([])
        self.mti_1_coordinate = np.array([])
        self.mti_2_coordinate = np.array([])
        
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
        self.mti_1_elevation_point = None
        self.mti_1_azimuth_point = None
        self.mti_2_elevation_point = None
        self.mti_2_azimuth_point = None
        
        
        # Graphic items
        self.elevation_runway_item = None
        self.azimuth_runway_item = None
        self.elevation_y_axis_item = None
        self.elevation_x_axis_item = None
        self.azimuth_y_axis_item = None
        self.azimuth_x_axis_item = None
        self.glideslope_item = None
        self.elevation_coverage_item = None
        self.azimuth_coverage_item = None
        self.elevation_gca_item = None
        self.azimuth_gca_item = None
        self.az_ant_elevation_item = None
        self.textinfo_item = None
        
        self.item_el = None
        self.item_az = None
        
        # Z Values
        self.axis_zvalue = 0.5
        self.runway_zvalue = 3.0
        self.gca_zvalue = 2.5
        self.coverage_zvalue = 2.5
        self.az_ant_elevation_zvalue = 2.5
        self.glideslope_zvalue = 2.0
        self.historic_plot_zvalue = 9.0
        self.plot_zvalue = 10.0
        
        self.decisionheight_zvalue = self.glideslope_zvalue

        # Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.periodic)
        self.timer.start(1000)


    # METHODS



    # Radar Control buttons
    
    def toggleRadiation(self, button):          # To model?
        self.radiation_active = button.inverted
        print 'toggle radiate'
        
    def toggleAntennaDrive(self, button):       # To model?
        self.antennadrive_active = button.inverted
        print 'toggle antennadrive'
        
    def toggleRainMode(self, button):
        self.rainmode_active = button.inverted  # Send to model???
        print 'toggle rainmode'
        
    def toggleMaintMode(self, button):
        self.maintmode_active = button.inverted
        print 'toggle maintmode'
        

    # Display Control buttons

    def toggleWx(self, button):
        self.wx_active = button.inverted
        print 'toggle wx'

    def toggleObs(self, button):
        self.obs_active = button.inverted
        print 'toggle obs'

    def toggleMap(self, button):
        self.map_active = button.inverted
        print 'toggle map'

    def toggleWhi(self, button):
        self.whi_active = button.inverted
        print 'toggle whi'

    def toggleRadarCover(self, button):
        self.radarcover_active = button.inverted
        self.drawElevationCoverage()
        self.drawAzimuthCoverage()
        self.drawAzAntElev()

    def toggleHist(self, button):
        self.hist_active = button.inverted
        print 'toggle hist'

    def toggleSynVideo(self, button):
        self.synvid_active = button.inverted
        print 'toggle syn vid'










    def periodic(self):
        self.drawTextInfo()

    def processReceivedPlot(self, airplane_coordinate, threshold_coordinate, eor_coordinate, gca_coordinate, mti_1_coordinate, mti_2_coordinate):

        self.airplane_coordinate = airplane_coordinate
        self.threshold_coordinate = threshold_coordinate
        self.eor_coordinate = eor_coordinate
        self.gca_coordinate = gca_coordinate
        self.mti_1_coordinate = mti_1_coordinate
        self.mti_2_coordinate = mti_2_coordinate

        self.calculatePoints()

        self.drawElevationGraphics()
        self.drawAzimuthGraphics()

        self.drawTextInfo()

        self.drawPlot()

    def calculatePoints(self):
        self.touchdown_elevation_point, self.touchdown_azimuth_point = self.getPoints(np.array([0.0, 0.0, 0.0]))
        self.airplane_elevation_point, self.airplane_azimuth_point = self.getPoints(self.airplane_coordinate)
        self.threshold_elevation_point, self.threshold_azimuth_point = self.getPoints(self.threshold_coordinate)
        self.eor_elevation_point, self.eor_azimuth_point = self.getPoints(self.eor_coordinate)
        self.gca_elevation_point, self.gca_azimuth_point = self.getPoints(self.gca_coordinate)
        self.mti_1_elevation_point, self.mti_1_azimuth_point = self.getPoints(self.mti_1_coordinate)
        self.mti_2_elevation_point, self.mti_2_azimuth_point = self.getPoints(self.mti_2_coordinate)

    def newAirport(self, airport):
        self.active_airport = airport


    def drawElevationGraphics(self):
        
        self.calculatePoints()  # Hmmmmmmmmmmmmmmm
        
        self.drawElevationRunway()
        self.drawGlideSlope()
        self.drawElevationGCA()
        self.drawElevationCoverage()
        self.drawAzAntElev()

    
    def drawAzimuthGraphics(self):
        
        self.calculatePoints()
        
        self.drawAzimuthRunway()
        self.drawAzimuthGCA()
        self.drawAzimuthCoverage()




    def drawMapSymbols(self):
        
        if self.mapsymbols_item:
            self.removeItem(self.mapsymbols_item)
            del self.mapsymbols_item
            
        if self.map_active:
            
            self.mapsymbols_item = QtGui.QGraphicsItemGroup(parent=None, scene=self)
            
            lineitem = QtGui.QGraphicsLineItem(0.0, 0.0, 100.0, 100.0, parent=self.mapsymbols_item)
            lineitem.setPen(self.axis_pen)
            
            



    def drawTextInfo(self):
            
        if self.textinfo_item:
            self.removeItem(self.textinfo_item)
            del self.textinfo_item

        if self.glideslope:
            gs_text = str(self.glideslope)
        else:
            gs_text = ''
            
        dh_text = '0 FT'        # Hmmm.... How to do the DH?????
            
        if self.active_airport != None and self.active_runway != None:
            try:
                rwy_direction_text = str(self.active_airport.runways[self.active_runway]['true'])
            except Exception:
                #print e
                rwy_direction_text = '---'
        else:
            rwy_direction_text = ''
            
        time_text = time.strftime('%H:%M:%S', time.gmtime())


        #if self.active_airport and self.glideslope:

        self.textinfo_item = QtGui.QGraphicsSimpleTextItem('GS: ' + gs_text, parent=None, scene=self)
        self.textinfo_item.setFont(self.textinfo_font)
        self.textinfo_item.setBrush(self.textinfo_brush)
        #textitemwidth = self.textinfo_item.boundingRect().width()
        #textitemheight = self.textinfo_item.boundingRect().height()
        self.textinfo_item.setPos(self.textgraphicsareatopleft_x + 1.0*self.textgraphicsareawidth/8, self.textgraphicsareatopleft_y)

        rwytextinfo_item = QtGui.QGraphicsSimpleTextItem('RWY: ' + rwy_direction_text, parent=self.textinfo_item)#, scene=self)
        rwytextinfo_item.setFont(self.textinfo_font)
        rwytextinfo_item.setBrush(self.textinfo_brush)
        #textitemwidth = self.textinfo_item.boundingRect().width()
        #textitemheight = self.textinfo_item.boundingRect().height()
        rwytextinfo_item.setPos(1.0*self.textgraphicsareawidth/8, 0.0) #self.textgraphicsareatopleft_y)

        dhtextinfo_item = QtGui.QGraphicsSimpleTextItem('DH: ' + dh_text, parent=self.textinfo_item)#, scene=self)
        dhtextinfo_item.setFont(self.textinfo_font)
        dhtextinfo_item.setBrush(self.textinfo_brush)
        #textitemwidth = self.textinfo_item.boundingRect().width()
        #textitemheight = self.textinfo_item.boundingRect().height()
        dhtextinfo_item.setPos(2.0*self.textgraphicsareawidth/8, 0.0) #self.textgraphicsareatopleft_y)

        timetextinfo_item = QtGui.QGraphicsSimpleTextItem('TIME: ' + time_text, parent=self.textinfo_item)#, scene=self)
        timetextinfo_item.setFont(self.textinfo_font)
        timetextinfo_item.setBrush(self.textinfo_brush)
        #textitemwidth = self.textinfo_item.boundingRect().width()
        #textitemheight = self.textinfo_item.boundingRect().height()
        timetextinfo_item.setPos(3.0*self.textgraphicsareawidth/8, 0.0) #self.textgraphicsareatopleft_y)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        


    def drawAzAntElev(self):
        if self.az_ant_elevation_item:
            self.removeItem(self.az_ant_elevation_item)
            del self.az_ant_elevation_item
            self.az_ant_elevation_item = None

        if self.rangescale and self.elevationscale and self.gca_elevation_point and (self.azantelev != None) and self.radarcover_active:

            m_per_x_pixel = self.rangescale*1852.0 / (self.rangeaxismax_x - self.rangeaxiszero_x)
            m_per_y_pixel = self.elevationscale*0.3048 / (self.elevationaxiszero_y - self.elevationaxismax_y)

            start_point = self.gca_elevation_point

            #print self.azantelev

            slope = np.tan(self.azantelev*np.pi/180) * m_per_x_pixel / m_per_y_pixel
            end_point = QtCore.QPointF(self.rangeaxismax_x, start_point.y() - slope*(self.rangeaxismax_x - self.gca_elevation_point.x()))
            line = QtCore.QLineF(start_point, end_point)

            self.az_ant_elevation_item = QtGui.QGraphicsLineItem(line, parent=None, scene=self)
            self.az_ant_elevation_item.setPen(self.az_ant_elevation_pen)
            self.az_ant_elevation_item.setZValue(self.az_ant_elevation_zvalue)


    def drawElevationCoverage(self):
        if self.elevation_coverage_item:
            self.removeItem(self.elevation_coverage_item)
            del self.elevation_coverage_item
            self.elevation_coverage_item = None
            
        if self.rangescale and self.elevationscale and self.gca_elevation_point and self.radarcover_active:
        
            m_per_x_pixel = self.rangescale*1852.0 / (self.rangeaxismax_x - self.rangeaxiszero_x)
            m_per_y_pixel = self.elevationscale*0.3048 / (self.elevationaxiszero_y - self.elevationaxismax_y)
            
            start_point = self.gca_elevation_point
            
            slope = np.tan(7.0*np.pi/180) * m_per_x_pixel / m_per_y_pixel
            upper_end_point = QtCore.QPointF(self.rangeaxismax_x, start_point.y() - slope*(self.rangeaxismax_x - self.gca_elevation_point.x()))
            upper_line = QtCore.QLineF(start_point, upper_end_point)
            
            self.elevation_coverage_item = QtGui.QGraphicsLineItem(upper_line, parent=None, scene=self)
            self.elevation_coverage_item.setPen(self.coverage_pen)
            self.elevation_coverage_item.setZValue(self.coverage_zvalue)
            
            slope = np.tan(-1.0*np.pi/180) * m_per_x_pixel / m_per_y_pixel
            lower_end_point = QtCore.QPointF(self.rangeaxismax_x, start_point.y() - slope*(self.rangeaxismax_x - self.gca_elevation_point.x()))
            
            # Keep lower coverage line inside the elevation graphics area
            if lower_end_point.y() > self.elevationgraphicsareabottomright_y:
                new_x = -1.0 * (self.elevationgraphicsareabottomright_y - start_point.y()) / slope + start_point.x()
                if new_x > self.rangeaxismax_x:
                    new_x = self.rangeaxismax_x
                
                delta_x = new_x - start_point.x()
                
                lower_end_point = QtCore.QPointF(new_x, start_point.y() - slope*delta_x)
                
            lower_line = QtCore.QLineF(start_point, lower_end_point)
            
            lower_line_item = QtGui.QGraphicsLineItem(lower_line, parent=self.elevation_coverage_item)
            lower_line_item.setPen(self.coverage_pen)
            lower_line_item.setZValue(self.coverage_zvalue)



    def drawAzimuthCoverage(self):
        if self.azimuth_coverage_item:
            self.removeItem(self.azimuth_coverage_item)
            del self.azimuth_coverage_item
            self.azimuth_coverage_item = None
            
        if self.rangescale and self.elevationscale and self.gca_azimuth_point and self.radarcover_active:
        
            m_per_x_pixel = self.rangescale*1852.0 / (self.rangeaxismax_x - self.rangeaxiszero_x)
            m_per_y_pixel = self.azimuthscale*0.3048 / (self.azimuthaxiszero_y - self.azimuthaxismax_y)
        
            start_point = self.gca_azimuth_point
            
            slope = np.tan(15.0*np.pi/180) * m_per_x_pixel / m_per_y_pixel
            delta_x = self.rangeaxismax_x - start_point.x()
            
            upper_end_point = QtCore.QPointF(self.rangeaxismax_x, start_point.y() - slope*delta_x)
            
            # Keep upper coverage line inside the azimuth graphics area
            if upper_end_point.y() < self.azimuthgraphicsareatopleft_y:

                new_x = -1.0 * (self.azimuthgraphicsareatopleft_y - start_point.y()) / slope + start_point.x()
                if new_x > self.rangeaxismax_x:
                    new_x = self.rangeaxismax_x
                
                delta_x = new_x - start_point.x()
                upper_end_point = QtCore.QPointF(new_x, start_point.y() - slope*delta_x)
            
            upper_line = QtCore.QLineF(start_point, upper_end_point)
            
            self.azimuth_coverage_item = QtGui.QGraphicsLineItem(upper_line, parent=None, scene=self)
            self.azimuth_coverage_item.setPen(self.coverage_pen)
            self.azimuth_coverage_item.setZValue(self.coverage_zvalue)
            
            lower_end_point = QtCore.QPointF(self.rangeaxismax_x, start_point.y() + slope*(self.rangeaxismax_x - self.gca_azimuth_point.x()))
            lower_line = QtCore.QLineF(start_point, lower_end_point)
            
            lower_line_item = QtGui.QGraphicsLineItem(lower_line, parent=self.azimuth_coverage_item)
            lower_line_item.setPen(self.coverage_pen)
            lower_line_item.setZValue(self.coverage_zvalue)
            
            middle_end_point = QtCore.QPointF(self.rangeaxismax_x, start_point.y())
            middle_line = QtCore.QLineF(start_point, middle_end_point)
            
            middle_line_item = QtGui.QGraphicsLineItem(middle_line, parent=self.azimuth_coverage_item)
            middle_line_item.setPen(self.coverage_pen)
            middle_line_item.setZValue(self.coverage_zvalue)
            
            

    def drawElevationGCA(self):
        if self.elevation_gca_item:
            self.removeItem(self.elevation_gca_item)
            del self.elevation_gca_item

            
        if self.gca_elevation_point:
            rect = QtCore.QRectF(self.gca_elevation_point.x()-7.5, self.gca_elevation_point.y()-10.0, 15.0, 10.0)
            self.elevation_gca_item = QtGui.QGraphicsRectItem(rect, parent=None, scene=self)
            self.elevation_gca_item.setBrush(self.gca_brush)
            self.elevation_gca_item.setZValue(self.gca_zvalue)
            
    def drawAzimuthGCA(self):
        if self.azimuth_gca_item:
            self.removeItem(self.azimuth_gca_item)
            del self.azimuth_gca_item

        if self.gca_azimuth_point:
            rect = QtCore.QRectF(self.gca_azimuth_point.x()-7.5, self.gca_azimuth_point.y()-5.0, 15.0, 10.0)
            self.azimuth_gca_item = QtGui.QGraphicsRectItem(rect, parent=None, scene=self)
            self.azimuth_gca_item.setBrush(self.gca_brush)
            self.azimuth_gca_item.setZValue(self.gca_zvalue)

    def getPoints(self, np_coord):
            
        if len(np_coord) == 3 and (self.azimuthscale != None) and (self.elevationscale != None):
            
            range_m = np_coord[0]
            altitude_m = np_coord[2]
            azimuth_m = np_coord[1]

            range_x_pixel = self.range_to_scenexcoord(range_m)
            altitude_y_pixel = self.altitude_to_sceneycoord(altitude_m)
            azimuth_y_pixel = self.azimuth_to_sceneycoord(azimuth_m)

            elev_point = QtCore.QPointF(range_x_pixel, altitude_y_pixel)
            azim_point = QtCore.QPointF(range_x_pixel, azimuth_y_pixel)

            return elev_point, azim_point
        else:
            return None, None



    def drawGlideSlope(self):
        if self.glideslope_item:
            self.removeItem(self.glideslope_item)
            del self.glideslope_item

        if self.glideslope and self.rangescale and self.touchdown_elevation_point:

            glideslope_end_coordinate = np.array([-1852.0*self.rangescale, 0.0, np.tan(self.glideslope*np.pi/180)*1852.0*self.rangescale])
            glideslope_end_point, _ = self.getPoints(glideslope_end_coordinate)
            line = QtCore.QLineF(self.touchdown_elevation_point, glideslope_end_point)
            
            self.glideslope_item = QtGui.QGraphicsLineItem(line, parent=None, scene=self)
            self.glideslope_item.setPen(self.glideslope_pen)
            self.glideslope_item.setZValue(self.glideslope_zvalue)

            if self.rangescale == 1:
                numberoffullmarkings = 6
            elif self.rangescale == 3:
                numberoffullmarkings = 4
            elif self.rangescale == 5:
                numberoffullmarkings = 6
            elif self.rangescale == 10:
                numberoffullmarkings = 6
            if self.rangescale == 15:
                numberoffullmarkings = 6
            elif self.rangescale == 20:
                numberoffullmarkings = 5

            slope = (glideslope_end_point.y() - self.touchdown_elevation_point.y()) / (glideslope_end_point.x() - self.touchdown_elevation_point.x())
            delta_x = (self.elevationrangeaxismax_x - self.elevationrangeaxiszero_x) / (numberoffullmarkings - 1)
            delta_y = delta_x * slope

            for c in range(numberoffullmarkings):
                x = self.elevationrangeaxiszero_x + c * delta_x
                y = self.elevationrangeaxis_y + c * delta_y
                lineitem = QtGui.QGraphicsLineItem(x, y + self.glideslopemarkinglength / 2, x, y - self.glideslopemarkinglength / 2, parent=self.glideslope_item)
                lineitem.setPen(self.glideslope_pen)



    def drawElevationRunway(self):
        # Remove possible existing elevation runway.
        if self.elevation_runway_item:
            self.removeItem(self.elevation_runway_item)
            del self.elevation_runway_item

        if self.eor_elevation_point and self.threshold_elevation_point:

            # Adjust the height in the eor point to have the same heiht as the threshold point.
            cheat_eor_elevation_point = QtCore.QPointF(self.eor_elevation_point)
            cheat_eor_elevation_point.setY(self.threshold_elevation_point.y())
            # This (above) is not correct, but it gives a nicer look.
        
            # Limit the drawing area leftwards
            if cheat_eor_elevation_point.x() < self.elevationminrangegraphicsrange:
                cheat_eor_elevation_point.setX(self.elevationminrangegraphicsrange)

            line = QtCore.QLineF(self.threshold_elevation_point, cheat_eor_elevation_point)
            self.elevation_runway_item = QtGui.QGraphicsLineItem(line, parent=None, scene=self)
            self.elevation_runway_item.setPen(self.runway_pen)
            self.elevation_runway_item.setZValue(self.runway_zvalue)
                        
            textitem = QtGui.QGraphicsSimpleTextItem(self.active_airport.runways[self.active_runway]['name'], parent=self.elevation_runway_item)
            
            textitem.setFont(self.textinfo_font)
            textitem.setBrush(self.textinfo_brush)
            textitemwidth = textitem.boundingRect().width()
            textitemheight = textitem.boundingRect().height()
            textitem.setPos(self.elevationgraphicsareatopleft_x, self.elevationrangeaxis_y - textitemheight / 2)
            
            painterpath = QtGui.QPainterPath()
            painterpath.addEllipse(self.threshold_elevation_point.x() - 3.0, self.threshold_elevation_point.y(), 6.0, 20.0)
            painterpath.addEllipse(self.threshold_elevation_point.x() - 3.0, self.threshold_elevation_point.y() - 20.0, 6.0, 20.0)
        
            self.path_item = QtGui.QGraphicsPathItem(painterpath, parent=self.elevation_runway_item, scene=self)
            self.path_item.setPen(self.runway_pen)

            # Make this a bit nicer perhaps


    def drawAzimuthRunway(self):
        if self.azimuth_runway_item:
            self.removeItem(self.azimuth_runway_item)
            del self.azimuth_runway_item
        
        if self.eor_azimuth_point and self.threshold_azimuth_point:
        
            modified_eor_azimuth_point = QtCore.QPointF(self.eor_azimuth_point)
            if self.eor_azimuth_point.x() < self.azimuthminrangegraphicsrange:
                modified_eor_azimuth_point.setX(self.azimuthminrangegraphicsrange)
        
            line = QtCore.QLineF(self.threshold_azimuth_point, modified_eor_azimuth_point)
            self.azimuth_runway_item = QtGui.QGraphicsLineItem(line, parent=None, scene=self)
            self.azimuth_runway_item.setPen(self.runway_pen)
            self.azimuth_runway_item.setZValue(self.runway_zvalue)
        
            textitem = QtGui.QGraphicsSimpleTextItem(self.active_airport.runways[self.active_runway]['name'], parent=self.elevation_runway_item)
            textitem.setFont(self.textinfo_font)
            textitem.setBrush(self.textinfo_brush)
            textitemwidth = textitem.boundingRect().width()
            textitemheight = textitem.boundingRect().height()
            textitem.setPos(self.azimuthgraphicsareatopleft_x, self.azimuthrangeaxis_y - textitemheight / 2)

            painterpath = QtGui.QPainterPath()
            painterpath.addEllipse(self.threshold_azimuth_point.x() - 3.0, self.threshold_azimuth_point.y(), 6.0, 20.0)
            painterpath.addEllipse(self.threshold_azimuth_point.x() - 3.0, self.threshold_azimuth_point.y() - 20.0, 6.0, 20.0)
        
            self.path_item = QtGui.QGraphicsPathItem(painterpath, parent=self.azimuth_runway_item, scene=self)
            self.path_item.setPen(self.runway_pen)
            
            
            # Make this a bit nicer perhaps



    #def drawElevationTrackPlot(self):
        


    
    def drawPlot(self):
        # Draw the plot

        if self.airplane_elevation_point and self.airplane_azimuth_point:

            self.brush = QtGui.QBrush(QtCore.Qt.white)

            if self.item_el:
                self.removeItem(self.item_el)
                self.item_el = None

            #if range_x_pixel and altitude_y_pixel:
            
            
            self.item_el = QtGui.QGraphicsEllipseItem(self.airplane_elevation_point.x()-4.0, self.airplane_elevation_point.y()-4.0, 8.0, 8.0, parent=None, scene=self)
            self.item_el.setBrush(self.brush)
            self.item_el.setZValue(self.plot_zvalue)
        
            if self.item_az:
                self.removeItem(self.item_az)
                self.item_az = None

            #if range_x_pixel and azimuth_y_pixel:
            self.item_az = QtGui.QGraphicsEllipseItem(self.airplane_azimuth_point.x()-4.0, self.airplane_azimuth_point.y()-4.0, 8.0, 8.0, parent=None, scene=self)
            self.item_az.setBrush(self.brush)
            self.item_az.setZValue(self.plot_zvalue)









    
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


    def dostuff(self):
        self.rect = QtGui.QGraphicsRectItem(self.textgraphicsareatopleft_x, self.textgraphicsareatopleft_y, self.textgraphicsareawidth, self.textgraphicsareaheight, scene=self)
        self.rect.setPen(QtGui.QPen(QtCore.Qt.darkGray))















    # AXIS GRAPHICS METHODS

    def createElevationAxis(self):
        
        if self.elevation_y_axis_item:
            self.removeItem(self.elevation_y_axis_item)
            del self.elevation_y_axis_item
        
        line = QtCore.QLineF(self.elevationaxis_x, self.elevationaxismax_y, self.elevationaxis_x, self.elevationaxismin_y)
        self.elevation_y_axis_item = QtGui.QGraphicsLineItem(line, parent=None, scene=self)
        self.elevation_y_axis_item.setPen(self.axis_pen)
        
        x = self.elevationaxis_x
        delta_y = (self.elevationaxismax_y - self.elevationaxiszero_y) / 4
        for c in range(1, 5):

            y = self.elevationaxiszero_y + c * delta_y

            lineitem = QtGui.QGraphicsLineItem(x - self.axismarkinglength / 2,  y, x + self.axismarkinglength / 2, y, parent=self.elevation_y_axis_item)
            lineitem.setPen(self.axis_pen)

            text = str(c * self.elevationscale / 4)
            textitem = QtGui.QGraphicsSimpleTextItem(text, parent=self.elevation_y_axis_item)
            textitem.setFont(self.axis_font)
            textitem.setBrush(self.axis_color)
            textitemwidth = textitem.boundingRect().width()
            textitemheight = textitem.boundingRect().height()
            if c == 4:
                textitem.setPos(self.elevationgraphicsareatopleft_x, y)
            else:
                textitem.setPos(self.elevationgraphicsareatopleft_x, y - textitemheight / 2)

        y = self.elevationaxiszero_y - delta_y / 2
        lineitem = QtGui.QGraphicsLineItem(x - self.axismarkinglength / 2,  y, x + self.axismarkinglength / 2, y, parent=self.elevation_y_axis_item)
        lineitem.setPen(self.axis_pen)

        text = str(-1 * self.elevationscale / 8)
        textitem = QtGui.QGraphicsSimpleTextItem(text, parent=self.elevation_y_axis_item)
        textitem.setFont(self.axis_font)
        textitem.setBrush(self.axis_color)
        textitemwidth = textitem.boundingRect().width()
        textitemheight = textitem.boundingRect().height()
        textitem.setPos(0.0, y - textitemheight)
        
        if self.elevation_runway_item:
            self.drawElevationRunway()
            self.drawGlideSlope()


    def createAzimuthAxis(self):
        
        if self.azimuth_y_axis_item:
            self.removeItem(self.azimuth_y_axis_item)
            del self.azimuth_y_axis_item

        line = QtCore.QLineF(self.azimuthaxis_x, self.azimuthaxismax_y, self.azimuthaxis_x, self.azimuthaxismin_y)
        self.azimuth_y_axis_item = QtGui.QGraphicsLineItem(line, parent=None, scene=self)
        self.azimuth_y_axis_item.setPen(self.axis_pen)

        x = self.azimuthaxis_x
        delta_y = (self.azimuthaxismax_y - self.azimuthaxiszero_y) / 4

        for c in range(-4, 5):

            y = self.azimuthaxiszero_y + c * delta_y
            if c != 0:
                lineitem = QtGui.QGraphicsLineItem(x - self.axismarkinglength / 2,  y, x + self.axismarkinglength / 2, y, parent=self.azimuth_y_axis_item)
                lineitem.setPen(self.axis_pen)

                text = str(c * self.azimuthscale / 4)
                textitem = QtGui.QGraphicsSimpleTextItem(text, parent=self.azimuth_y_axis_item)
                textitem.setFont(self.axis_font)
                textitem.setBrush(self.axis_color)
                textitemwidth = textitem.boundingRect().width()
                textitemheight = textitem.boundingRect().height()
                if c == 4:
                    textitem.setPos(self.elevationgraphicsareatopleft_x, y)
                elif c == -4:
                    textitem.setPos(self.elevationgraphicsareatopleft_x, y - textitemheight)
                else:
                    textitem.setPos(self.elevationgraphicsareatopleft_x, y - textitemheight / 2)

        if self.azimuth_runway_item:
            self.drawAzimuthRunway()



    def createElevationAndAzimuthRangeAxis(self):
        
        if self.elevation_x_axis_item and self.azimuth_x_axis_item:     # Either both are 1 or both are 0
            self.removeItem(self.elevation_x_axis_item)
            self.removeItem(self.azimuth_x_axis_item)
            del self.elevation_x_axis_item
            del self.azimuth_x_axis_item
        
        self.elevation_x_axis_item = QtGui.QGraphicsLineItem(self.elevationrangeaxiszero_x, self.elevationrangeaxis_y, self.elevationrangeaxismax_x, self.elevationrangeaxis_y, scene=self)
        self.elevation_x_axis_item.setPen(self.axis_pen)
        self.elevation_x_axis_item.setZValue(self.axis_zvalue)

        self.azimuth_x_axis_item = QtGui.QGraphicsLineItem(self.azimuthrangeaxiszero_x, self.azimuthrangeaxis_y, self.azimuthrangeaxismax_x, self.azimuthrangeaxis_y, scene=self)
        self.azimuth_x_axis_item.setPen(self.axis_pen)
        self.azimuth_x_axis_item.setZValue(self.axis_zvalue)

        if self.rangescale == 1:
            numberoffullmarkings = 6
            markingtext = ['0', '0.2', '0.4', '0.6', '0.8', '1']
        elif self.rangescale == 3:
            numberoffullmarkings = 4
            markingtext = ['0', '1', '2', '3']
        elif self.rangescale == 5:
            numberoffullmarkings = 6
            markingtext = ['0', '1', '2', '3', '4', '5']
        elif self.rangescale == 10:
            numberoffullmarkings = 6
            markingtext = ['0', '2', '4', '6', '8', '10']
        if self.rangescale == 15:
            numberoffullmarkings = 6
            markingtext = ['0', '3', '6', '9', '12', '15']
        elif self.rangescale == 20:
            numberoffullmarkings = 5
            markingtext = ['0', '5', '10', '15', '20']

        delta_x = (self.elevationrangeaxismax_x - self.elevationrangeaxiszero_x) / (numberoffullmarkings - 1)
        
        for c in range(numberoffullmarkings):
            x = self.elevationrangeaxiszero_x + c * delta_x
            lineitem = QtGui.QGraphicsLineItem(x, self.elevationrangeaxis_y + self.axismarkinglength / 2, x, self.elevationrangeaxis_y - self.axismarkinglength / 2, parent=self.elevation_x_axis_item)
            lineitem.setPen(self.axis_pen)
            lineitem2 = QtGui.QGraphicsLineItem(x, self.azimuthrangeaxis_y + self.axismarkinglength / 2, x, self.azimuthrangeaxis_y - self.axismarkinglength / 2, parent=self.azimuth_x_axis_item)
            lineitem2.setPen(self.axis_pen)

            textitem = QtGui.QGraphicsSimpleTextItem(markingtext[c], parent=self.elevation_x_axis_item)
            textitem.setFont(self.axis_font)
            textitem.setBrush(self.axis_color)
            textitemwidth = textitem.boundingRect().width()
            textitemheight = textitem.boundingRect().height()
            if c == len(markingtext) - 1:
                textitem.setPos(x - textitemwidth, self.elevationrangeaxis_y + self.axismarkinglength / 2 + 4)
            else:
                textitem.setPos(x - textitemwidth / 2.0, self.elevationrangeaxis_y + self.axismarkinglength / 2 + 4)

            textitem2 = QtGui.QGraphicsSimpleTextItem(markingtext[c], parent=self.azimuth_x_axis_item)
            textitem2.setFont(self.axis_font)
            textitem2.setBrush(self.axis_color)
            textitemwidth = textitem2.boundingRect().width()
            textitemheight = textitem2.boundingRect().height()
            if c == len(markingtext) - 1:
                textitem2.setPos(x - textitemwidth, self.azimuthrangeaxis_y + self.axismarkinglength / 2 + 4)
            else:
                textitem2.setPos(x - textitemwidth / 2.0, self.azimuthrangeaxis_y + self.axismarkinglength / 2 + 4)

        if self.rangescale == 1:
            numberofhalfmarkings = numberoffullmarkings - 1
            for c in range(numberofhalfmarkings):
                x = self.elevationrangeaxiszero_x + c * delta_x
                line = QtGui.QGraphicsLineItem(x + delta_x / 2, self.elevationrangeaxis_y + self.axismarkinglength / 4, x + delta_x / 2, self.elevationrangeaxis_y - self.axismarkinglength / 4, parent=self.elevation_x_axis_item)
                line.setPen(self.axis_pen)
                line2 = QtGui.QGraphicsLineItem(x + delta_x / 2, self.azimuthrangeaxis_y + self.axismarkinglength / 4, x + delta_x / 2, self.azimuthrangeaxis_y - self.axismarkinglength / 4, parent=self.azimuth_x_axis_item)
                line2.setPen(self.axis_pen)





