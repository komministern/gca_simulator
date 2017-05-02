#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    Copyright © 2016, 2017 Oscar Franzén <oscarfranzen@yahoo.se>
#
#    This file is part of GCA Simulator.

from PySide import QtGui, QtCore
import numpy as np

class MyScene(QtGui.QGraphicsScene):

    scenetotaltopleft_x = 0.0
    scenetotaltopleft_y = 0.0
    scenetotalwidth = 1600
    scenetotalheight = 1200

    buttonwindowareawidth = 320
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

    elevationminrangegraphicsrange = elevationrangeaxiszero_x / 2

    # **** AZIMUTH RANGE AXIS

    azimuthrangeaxiszero_x = rangeaxiszero_x
    azimuthrangeaxismax_x = rangeaxismax_x
    azimuthrangeaxis_y = azimuthgraphicsareaheight / 2 + azimuthgraphicsareatopleft_y

    axismarkinglength = 16.0    # Absolute value
    
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
        self.axis_color = QtGui.QColor(255, 165, 0, 200)
        
        self.axis_pen = QtGui.QPen(self.axis_color)
        self.axis_pen.setWidth(2.0)

        self.runway_pen = QtGui.QPen(QtCore.Qt.darkCyan)
        self.runway_pen.setWidth(2)
        
        self.glideslope_pen = QtGui.QPen(QtCore.Qt.cyan)
        self.glideslope_pen.setWidth(2)

        # Attributes relevant for the display
        self.rangescale = None
        self.elevationscale = None
        self.azimuthscale = None
        self.glideslope = None

        # Windows related stuff
        self.movablewindowZval = 0.0
        self.activewindowtopborders = []
        
        
        # Points
        self.touchdown_elevation_point, self.touchdown_azimuth_point = None, None
        self.aiplane_elevation_point, self.airplane_azimuth_point = None, None
        self.threshold_elevation_point, self.threshold_azimuth_point = None, None
        self.eor_elevation_point, self.eor_azimuth_point = None, None
        self.gca_elevation_point, self.gca_azimuth_point = None, None
        self.mti_1_elevation_point, self.mti_1_azimuth_point = None, None
        self.mti_2_elevation_point, self.mti_2_azimuth_point = None, None
        
        
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
        
        self.item_el = None
        self.item_az = None
        
        # Z Values
        self.axis_zvalue = 0.0
        self.runway_zvalue = 1.0
        self.glideslope_zvalue = 2.0
        self.coverage_zvalue = 3.0
        self.historic_plot_zvalue = 9.0
        self.plot_zvalue = 10.0



    # METHODS


    def processReceivedPlot(self, airplane_coordinate, threshold_coordinate, eor_coordinate, gca_coordinate=np.array([]), mti_1_coordinate=np.array([]), mti_2_coordinate=np.array([])):

        self.touchdown_elevation_point, self.touchdown_azimuth_point = self.getPoints(np.array([0.0, 0.0, 0.0]))
        self.aiplane_elevation_point, self.airplane_azimuth_point = self.getPoints(airplane_coordinate)
        self.threshold_elevation_point, self.threshold_azimuth_point = self.getPoints(threshold_coordinate)
        self.eor_elevation_point, self.eor_azimuth_point = self.getPoints(eor_coordinate)
        self.gca_elevation_point, self.gca_azimuth_point = self.getPoints(gca_coordinate)
        self.mti_1_elevation_point, self.mti_1_azimuth_point = self.getPoints(mti_1_coordinate)
        self.mti_2_elevation_point, self.mti_2_azimuth_point = self.getPoints(mti_2_coordinate)

        self.drawElevationRunway()
        self.drawAzimuthRunway()
        
        self.drawGlideSlope()

        self.drawPlot()


    def getPoints(self, np_coord):
            
        if len(np_coord) == 3:
            
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

            delta_x = (self.elevationrangeaxismax_x - self.elevationrangeaxiszero_x) / (numberoffullmarkings - 1)

            for c in range(numberoffullmarkings):
                x = self.elevationrangeaxiszero_x + c * delta_x
                lineitem = QtGui.QGraphicsLineItem(x, np.tan(self.glideslope*np.pi/180)*c*delta_x + self.axismarkinglength / 2, x, np.tan(self.glideslope*np.pi/180)*c*delta_x - self.axismarkinglength / 2, parent=self.glideslope_item)
                lineitem.setPen(self.glideslope_pen)



    def drawElevationRunway(self):
        # Remove possible existing elevation runway.
        if self.elevation_runway_item:
            self.removeItem(self.elevation_runway_item)
            del self.elevation_runway_item

        # Adjust the height in the eor point to have the same heiht as the threshold point.
        cheat_eor_elevation_point = QtCore.QPointF(self.eor_elevation_point)
        cheat_eor_elevation_point.setY(self.threshold_elevation_point.y())
        # This (above) is not correct, but it gives a nicer look.

        line = QtCore.QLineF(self.threshold_elevation_point, cheat_eor_elevation_point)
        self.elevation_runway_item = QtGui.QGraphicsLineItem(line, parent=None, scene=self)
        self.elevation_runway_item.setPen(self.runway_pen)
        self.elevation_runway_item.setZValue(self.runway_zvalue)

        # Draw text here.
            


    def drawAzimuthRunway(self):
        if self.azimuth_runway_item:
            self.removeItem(self.azimuth_runway_item)
            del self.azimuth_runway_item
            
        line = QtCore.QLineF(self.threshold_azimuth_point, self.eor_azimuth_point)
        self.azimuth_runway_item = QtGui.QGraphicsLineItem(line, parent=None, scene=self)
        self.azimuth_runway_item.setPen(self.runway_pen)
        self.azimuth_runway_item.setZValue(self.runway_zvalue)
        
        # Draw text here.


        

    
    def drawPlot(self):
        # Draw the plot

        if self.airplane_coordinate.any():      # ?????

            range_m = self.airplane_coordinate[0]
            altitude_m = self.airplane_coordinate[2]
            azimuth_m = self.airplane_coordinate[1]

            range_x_pixel = self.range_to_scenexcoord(range_m)
            altitude_y_pixel = self.altitude_to_sceneycoord(altitude_m)
            azimuth_y_pixel = self.azimuth_to_sceneycoord(azimuth_m)

            self.brush = QtGui.QBrush(QtCore.Qt.white)

            if self.item_el:
                self.removeItem(self.item_el)
                self.item_el = None

            if range_x_pixel and altitude_y_pixel:
                self.item_el = QtGui.QGraphicsEllipseItem(range_x_pixel-4.0, altitude_y_pixel-4.0, 8.0, 8.0, parent=None, scene=self)
                self.item_el.setBrush(self.brush)
                self.item_el.setZValue(self.plot_zvalue)
        
            if self.item_az:
                self.removeItem(self.item_az)
                self.item_az = None

            if range_x_pixel and azimuth_y_pixel:
                self.item_az = QtGui.QGraphicsEllipseItem(range_x_pixel-4.0, azimuth_y_pixel-4.0, 8.0, 8.0, parent=None, scene=self)
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

