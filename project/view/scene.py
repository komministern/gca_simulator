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

        # Constants
        self.axisfont = QtGui.QFont("Helvetica", 10)
        self.axiscolor = QtGui.QColor(255, 165, 0, 200)
        self.axispen = QtGui.QPen(self.axiscolor)
        self.axispen.setWidth(2.0)

        # Attributes
        self.rangescale = None
        self.elevationscale = None
        self.azimuthscale = None

        self.movablewindowZval = 0.0
        self.activewindowtopborders = [] 

        self.item_el = None
        self.item_az = None

        self.last_threshold_coordinate = []
        self.last_eor_coordinate = []
        self.last_airplane_coordinate = []




    # METHODS


    def processReceivedPlot(self, airplane_coordinate, threshold_coordinate, eor_coordinate):

        #self.drawRunway(self, self.model.p_thr1, self.model.p_thr2)

        self.drawLine(threshold_coordinate, eor_coordinate)

#        print airplane_coordinate
#        print threshold_coordinate
#        print eor_coordinate

        self.last_threshold_coordinate = threshold_coordinate
        self.last_eor_coordinate = eor_coordinate
        self.last_airplane_coordinate = airplane_coordinate

        range_m = airplane_coordinate[0]
        altitude_m = airplane_coordinate[2]
        azimuth_m = airplane_coordinate[1]

        range_x_pixel = self.range_to_scenexcoord(range_m)
        altitude_y_pixel = self.altitude_to_sceneycoord(altitude_m)
        azimuth_y_pixel = self.azimuth_to_sceneycoord(azimuth_m)
 
#        print 'range: scene x coordinate: '
#        print range_x_pixel
#        print 'altitude: scene y coordinate'
#        print altitude_y_pixel
#        print 'azimuth: scene y coordinate'
#        print azimuth_y_pixel

        self.brush = QtGui.QBrush(QtCore.Qt.white)

        if self.item_el:
            self.removeItem(self.item_el)
            self.item_el = None

        if range_x_pixel and altitude_y_pixel:

            self.item_el = QtGui.QGraphicsEllipseItem(range_x_pixel-4.0, altitude_y_pixel-4.0, 8.0, 8.0, parent=None, scene=self)
            self.item_el.setBrush(self.brush)
        
        if self.item_az:
            self.removeItem(self.item_az)
            self.item_az = None

        if range_x_pixel and azimuth_y_pixel:

            self.item_az = QtGui.QGraphicsEllipseItem(range_x_pixel-4.0, azimuth_y_pixel-4.0, 8.0, 8.0, parent=None, scene=self)
            self.item_az.setBrush(self.brush)

#        self.drawLine(threshold_coordinate, eor_coordinate)

    
    def range_to_scenexcoord(self, range_m):
        # input in m
        # 1 nmi is 1852 m

        #   range_nmi   scene
        #   0.0         rangeaxiszero_x
        #   max         rangeaxixmax_x

        # elevationminrangegraphicsrange is largest negative scene x-coordinate to be plotted.
        range_nmi = -1.0 * range_m / 1852.0
        nmi_per_pixel = self.rangescale / (self.rangeaxismax_x - self.rangeaxiszero_x)
        smallest_range_nmi_to_be_plotted = nmi_per_pixel * (self.elevationminrangegraphicsrange - self.rangeaxiszero_x)
        if range_nmi > smallest_range_nmi_to_be_plotted and range_nmi < self.rangescale:
            return self.rangeaxiszero_x + range_nmi / nmi_per_pixel
        else:
            return None


    def altitude_to_sceneycoord(self, altitude_m):
        # input in m
        # 1 m is 3.2808399 ft

        #   range_ft    scene
        #   0.0         elevationaxiszero_y
        #   max         elevationaxismax_y
        altitude_ft = 3.2808399 * altitude_m
        ft_per_pixel = self.elevationscale / (self.elevationaxismax_y - self.elevationaxiszero_y)
        smallest_elevation_ft_to_be_plotted = ft_per_pixel * (self.elevationaxismin_y - self.elevationaxiszero_y)


        if altitude_ft > smallest_elevation_ft_to_be_plotted and altitude_ft < self.elevationscale:
            return self.elevationaxiszero_y + altitude_ft / ft_per_pixel
        else:
            return None


    def azimuth_to_sceneycoord(self, azimuth_m):
        # input in m
        # 1 m is 3.2808399 ft

        #   range_ft    scene
        #   0.0         azimuthaxiszero_y
        #   max         azimuthaxismax_y
        #   min         azimuthaxismin_y
        azimuth_ft = 3.2808399 * azimuth_m
        ft_per_pixel = self.azimuthscale / (self.azimuthaxiszero_y - self.azimuthaxismax_y)
        #smallest_elevation_ft_to_be_plotted = ft_per_pixel * (self.elevationaxismin_y - self.elevationaxiszero_y)

        if abs(azimuth_ft) < self.azimuthscale:
            return self.azimuthaxiszero_y + azimuth_ft / ft_per_pixel
        else:
            return None








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


    # **** AXIS GRAPHICS METHODS


    def createElevationAxis(self, elevationscale):
        self.elevationaxislineitem = QtGui.QGraphicsLineItem(self.elevationaxis_x, self.elevationaxismax_y, self.elevationaxis_x, self.elevationaxismin_y, scene=self)
        self.elevationaxislineitem.setPen(self.axispen)

        x = self.elevationaxis_x
        delta_y = (self.elevationaxismax_y - self.elevationaxiszero_y) / 4
        for c in range(1, 5):

            y = self.elevationaxiszero_y + c * delta_y

            lineitem = QtGui.QGraphicsLineItem(x - self.axismarkinglength / 2,  y, x + self.axismarkinglength / 2, y, parent=self.elevationaxislineitem)
            lineitem.setPen(self.axispen)

            text = str(c * elevationscale / 4)
            textitem = QtGui.QGraphicsSimpleTextItem(text, parent=self.elevationaxislineitem)
            textitem.setFont(self.axisfont)
            textitem.setBrush(self.axiscolor)
            textitemwidth = textitem.boundingRect().width()
            textitemheight = textitem.boundingRect().height()
            if c == 4:
                textitem.setPos(self.elevationgraphicsareatopleft_x, y)
            else:
                textitem.setPos(self.elevationgraphicsareatopleft_x, y - textitemheight / 2)

        y = self.elevationaxiszero_y - delta_y / 2
        lineitem = QtGui.QGraphicsLineItem(x - self.axismarkinglength / 2,  y, x + self.axismarkinglength / 2, y, parent=self.elevationaxislineitem)
        lineitem.setPen(self.axispen)

        text = str(-1 * elevationscale / 8)
        textitem = QtGui.QGraphicsSimpleTextItem(text, parent=self.elevationaxislineitem)
        textitem.setFont(self.axisfont)
        textitem.setBrush(self.axiscolor)
        textitemwidth = textitem.boundingRect().width()
        textitemheight = textitem.boundingRect().height()
        textitem.setPos(0.0, y - textitemheight)


    def createAzimuthAxis(self, azimuthscale):
        self.azimuthaxislineitem = QtGui.QGraphicsLineItem(self.azimuthaxis_x, self.azimuthaxismin_y, self.azimuthaxis_x, self.azimuthaxismax_y, scene=self)
        self.azimuthaxislineitem.setPen(self.axispen)

        x = self.azimuthaxis_x
        delta_y = (self.azimuthaxismax_y - self.azimuthaxiszero_y) / 4

        for c in range(-4, 5):

            y = self.azimuthaxiszero_y + c * delta_y
            if c != 0:
                lineitem = QtGui.QGraphicsLineItem(x - self.axismarkinglength / 2,  y, x + self.axismarkinglength / 2, y, parent=self.azimuthaxislineitem)
                lineitem.setPen(self.axispen)

                text = str(c * azimuthscale / 4)
                textitem = QtGui.QGraphicsSimpleTextItem(text, parent=self.azimuthaxislineitem)
                textitem.setFont(self.axisfont)
                textitem.setBrush(self.axiscolor)
                textitemwidth = textitem.boundingRect().width()
                textitemheight = textitem.boundingRect().height()
                if c == 4:
                    textitem.setPos(self.elevationgraphicsareatopleft_x, y)
                elif c == -4:
                    textitem.setPos(self.elevationgraphicsareatopleft_x, y - textitemheight)
                else:
                    textitem.setPos(self.elevationgraphicsareatopleft_x, y - textitemheight / 2)



    def createElevationAndAzimuthRangeAxis(self, rangescale):
        self.elevationrangeaxislineitem = QtGui.QGraphicsLineItem(self.elevationrangeaxiszero_x, self.elevationrangeaxis_y, self.elevationrangeaxismax_x, self.elevationrangeaxis_y, scene=self)
        self.elevationrangeaxislineitem.setPen(self.axispen)

        self.azimuthrangeaxislineitem = QtGui.QGraphicsLineItem(self.azimuthrangeaxiszero_x, self.azimuthrangeaxis_y, self.azimuthrangeaxismax_x, self.azimuthrangeaxis_y, scene=self)
        self.azimuthrangeaxislineitem.setPen(self.axispen)

        if rangescale == 1:
            numberoffullmarkings = 6
            markingtext = ['0', '0.2', '0.4', '0.6', '0.8', '1']
        elif rangescale == 3:
            numberoffullmarkings = 4
            markingtext = ['0', '1', '2', '3']
        elif rangescale == 5:
            numberoffullmarkings = 6
            markingtext = ['0', '1', '2', '3', '4', '5']
        elif rangescale == 10:
            numberoffullmarkings = 6
            markingtext = ['0', '2', '4', '6', '8', '10']
        if rangescale == 15:
            numberoffullmarkings = 6
            markingtext = ['0', '3', '6', '9', '12', '15']
        elif rangescale == 20:
            numberoffullmarkings = 5
            markingtext = ['0', '5', '10', '15', '20']

        delta_x = (self.elevationrangeaxismax_x - self.elevationrangeaxiszero_x) / (numberoffullmarkings - 1)
        
        for c in range(numberoffullmarkings):
            x = self.elevationrangeaxiszero_x + c * delta_x
            lineitem = QtGui.QGraphicsLineItem(x, self.elevationrangeaxis_y + self.axismarkinglength / 2, x, self.elevationrangeaxis_y - self.axismarkinglength / 2, parent=self.elevationrangeaxislineitem)
            lineitem.setPen(self.axispen)
            lineitem2 = QtGui.QGraphicsLineItem(x, self.azimuthrangeaxis_y + self.axismarkinglength / 2, x, self.azimuthrangeaxis_y - self.axismarkinglength / 2, parent=self.azimuthrangeaxislineitem)
            lineitem2.setPen(self.axispen)

            textitem = QtGui.QGraphicsSimpleTextItem(markingtext[c], parent=self.elevationrangeaxislineitem)
            textitem.setFont(self.axisfont)
            textitem.setBrush(self.axiscolor)
            textitemwidth = textitem.boundingRect().width()
            textitemheight = textitem.boundingRect().height()
            if c == len(markingtext) - 1:
                textitem.setPos(x - textitemwidth, self.elevationrangeaxis_y + self.axismarkinglength / 2 + 4)
            else:
                textitem.setPos(x - textitemwidth / 2.0, self.elevationrangeaxis_y + self.axismarkinglength / 2 + 4)

            textitem2 = QtGui.QGraphicsSimpleTextItem(markingtext[c], parent=self.azimuthrangeaxislineitem)
            textitem2.setFont(self.axisfont)
            textitem2.setBrush(self.axiscolor)
            textitemwidth = textitem2.boundingRect().width()
            textitemheight = textitem2.boundingRect().height()
            if c == len(markingtext) - 1:
                textitem2.setPos(x - textitemwidth, self.azimuthrangeaxis_y + self.axismarkinglength / 2 + 4)
            else:
                textitem2.setPos(x - textitemwidth / 2.0, self.azimuthrangeaxis_y + self.axismarkinglength / 2 + 4)

        if rangescale == 1:
            numberofhalfmarkings = numberoffullmarkings - 1
            for c in range(numberofhalfmarkings):
                x = self.elevationrangeaxiszero_x + c * delta_x
                line = QtGui.QGraphicsLineItem(x + delta_x / 2, self.elevationrangeaxis_y + self.axismarkinglength / 4, x + delta_x / 2, self.elevationrangeaxis_y - self.axismarkinglength / 4, parent=self.elevationrangeaxislineitem)
                line.setPen(self.axispen)
                line2 = QtGui.QGraphicsLineItem(x + delta_x / 2, self.azimuthrangeaxis_y + self.axismarkinglength / 4, x + delta_x / 2, self.azimuthrangeaxis_y - self.axismarkinglength / 4, parent=self.azimuthrangeaxislineitem)
                line2.setPen(self.axispen)

        if self.last_threshold_coordinate != [] and self.last_eor_coordinate != []:
            self.removeItem(self.line)
            self.drawLine(self.last_threshold_coordinate, self.last_eor_coordinate)



    def drawLine(self, p1, p2, pen=None):

        p1_range_m = p1[0]
        p1_altitude_m = p1[2]
        p1_azimuth_m = p1[1]

        p2_range_m = p2[0]
        p2_altitude_m = p2[2]
        p2_azimuth_m = p2[1]

        p1_range_x_pixel = self.range_to_scenexcoord(p1_range_m)
        p1_altitude_y_pixel = self.altitude_to_sceneycoord(p1_altitude_m)
        p1_azimuth_y_pixel = self.azimuth_to_sceneycoord(p1_azimuth_m)

        p2_range_x_pixel = self.range_to_scenexcoord(p2_range_m)
        p2_altitude_y_pixel = self.altitude_to_sceneycoord(p2_altitude_m)
        p2_azimuth_y_pixel = self.azimuth_to_sceneycoord(p2_azimuth_m)

        if p1_range_x_pixel < self.elevationminrangegraphicsrange:
            p1_range_x_pixel = self.elevationminrangegraphicsrange

        if p2_range_x_pixel < self.elevationminrangegraphicsrange:
            p2_range_x_pixel = self.elevationminrangegraphicsrange

        self.line = QtGui.QGraphicsLineItem(p1_range_x_pixel, self.elevationrangeaxis_y, p2_range_x_pixel, self.elevationrangeaxis_y, parent=None, scene=self)
        pen = QtGui.QPen(QtCore.Qt.darkCyan)
        self.line.setPen(pen)


