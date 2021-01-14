"""
Copyright (C) 2021 Oscar Franzén <oscarfranzen@protonmail.com>

This file is part of GCA Simulator.

GCA Simulator is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

GCA Simulator is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with GCA Simulator.  If not, see <https://www.gnu.org/licenses/>.
"""

from PySide2 import QtCore, QtWidgets, QtGui

from .azimuthscaletextitem import AzimuthScaleTextItem


#class ElevationAxis(QtCore.QObject):
class ElevationAxis(QtWidgets.QGraphicsItemGroup):
    
    def __init__(self, scene):
        super(ElevationAxis, self).__init__()
        
        self.scene = scene

        self.scene.addItem(self)

        self.elevation_y_axis_item = None
        
        self.setZValue(self.scene.axis_zvalue)
        
        self.create()


    def draw(self):
        
        self.create()


    def create(self):
        
        if self.elevation_y_axis_item:

            self.scene.removeItem(self)

            #self.scene.removeItem(self.elevation_y_axis_item)
            self.removeFromGroup(self.elevation_y_axis_item)
            
            self.elevation_y_axis_item = None

            self.scene.addItem(self)

        if self.scene.elevationscale and self.scene.rangescale:

            line = QtCore.QLineF(self.scene.elevationaxis_x, self.scene.elevationaxismax_y, self.scene.elevationaxis_x, self.scene.elevationaxismin_y)
            self.elevation_y_axis_item = QtWidgets.QGraphicsLineItem(line)
            self.elevation_y_axis_item.setPen(self.scene.axis_pen)
        
            x = self.scene.elevationaxis_x
            delta_y = (self.scene.elevationaxismax_y - self.scene.elevationaxiszero_y) / 4
            for c in range(1, 5):

                y = self.scene.elevationaxiszero_y + c * delta_y

                lineitem = QtWidgets.QGraphicsLineItem(x - self.scene.axismarkinglength / 2,  y, x + self.scene.axismarkinglength / 2, y, parent=self.elevation_y_axis_item)
                lineitem.setPen(self.scene.axis_pen)

                text = str(c * self.scene.elevationscale // 4)
                textitem = QtWidgets.QGraphicsSimpleTextItem(text, parent=self.elevation_y_axis_item)
                textitem.setFont(self.scene.axis_font)
                textitem.setBrush(self.scene.axis_color)
                textitemwidth = textitem.boundingRect().width()
                textitemheight = textitem.boundingRect().height()
                if c == 4:
                    textitem.setPos(self.scene.elevationgraphicsareatopleft_x, y)

                    saved_width = textitemwidth
                    text = 'FT'
                    textitem = QtWidgets.QGraphicsSimpleTextItem(text, parent=self.elevation_y_axis_item)
                    textitem.setFont(self.scene.axis_font)
                    textitem.setBrush(self.scene.axis_color)
                    textitemwidth = textitem.boundingRect().width()
                    textitemheight = textitem.boundingRect().height()
                    textitem.setPos(self.scene.elevationgraphicsareatopleft_x + saved_width - textitemwidth, y + textitemheight)

                else:
                    textitem.setPos(self.scene.elevationgraphicsareatopleft_x, y - textitemheight / 2)

            y = self.scene.elevationaxiszero_y - delta_y / 2
            lineitem = QtWidgets.QGraphicsLineItem(x - self.scene.axismarkinglength / 2,  y, x + self.scene.axismarkinglength / 2, y, parent=self.elevation_y_axis_item)
            lineitem.setPen(self.scene.axis_pen)

            text = str(-1 * self.scene.elevationscale // 8)
            textitem = QtWidgets.QGraphicsSimpleTextItem(text, parent=self.elevation_y_axis_item)
            textitem.setFont(self.scene.axis_font)
            textitem.setBrush(self.scene.axis_color)
            textitemwidth = textitem.boundingRect().width()
            textitemheight = textitem.boundingRect().height()
            textitem.setPos(0.0, y - textitemheight)


            text = 'HAT'
            textitem = QtWidgets.QGraphicsSimpleTextItem(text, parent=self.elevation_y_axis_item)
            textitem.setFont(self.scene.axis_font)
            textitem.setBrush(self.scene.axis_color)
            textitemwidth = textitem.boundingRect().width()
            textitemheight = textitem.boundingRect().height()
            textitem.setPos(self.scene.elevationaxis_x + 20.0, self.scene.elevationaxismax_y + 5.0)

            #self.elevation_y_axis_item.setZValue(self.scene.axis_zvalue)

            self.addToGroup(self.elevation_y_axis_item)


            #self.addToGroup(self.elevation_y_axis_item)



class AzimuthAxis(QtWidgets.QGraphicsItemGroup):
#class AzimuthAxis(QtCore.QObject):
    
    def __init__(self, scene):
        super(AzimuthAxis, self).__init__()

        self.scene = scene

        self.scene.addItem(self)
        
        self.azimuth_y_axis_item = None
        
        self.setZValue(self.scene.axis_zvalue)
        
        
        #self.setHandlesChildEvents(False)              -------------------------------------------------------------------------------------------------------------------------------------------

        self.create()


    def draw(self):
        
        self.create()


    def create(self):
        
        if self.azimuth_y_axis_item:

            self.scene.removeItem(self)

            self.removeFromGroup(self.azimuth_y_axis_item)

            #self.removeFromGroup(self.azimuth_y_axis_item)
            self.azimuth_y_axis_item = None

            self.scene.addItem(self)

        if self.scene.azimuthscale and self.scene.rangescale:

            x = self.scene.azimuthaxis_x
            delta_y = (self.scene.azimuthaxismax_y - self.scene.azimuthaxiszero_y) / 4

            az_offset = self.scene.az_offset     # -4..4

            #self.scene.azimuthrangeaxis_y = self.scene.azimuthgraphicsareaheight / 2 + self.scene.azimuthgraphicsareatopleft_y - az_offset * delta_y
            #self.scene.azimuthaxiszero_y = self.scene.azimuthrangeaxis_y

            #azimuthrangeaxis_y = azimuthgraphicsareaheight / 2 + azimuthgraphicsareatopleft_y
            #azimuthaxiszero_y = azimuthrangeaxis_y

            line = QtCore.QLineF(self.scene.azimuthaxis_x, self.scene.azimuthaxismax_y, self.scene.azimuthaxis_x, self.scene.azimuthaxismin_y)
            self.azimuth_y_axis_item = QtWidgets.QGraphicsLineItem(line)
            self.azimuth_y_axis_item.setPen(self.scene.axis_pen)

            for position in range(-4, 5):

                y = self.scene.azimuthaxiszero_y + position * delta_y
                if position != az_offset:
                    lineitem = QtWidgets.QGraphicsLineItem(x - self.scene.axismarkinglength / 2,  y, x + self.scene.axismarkinglength / 2, y, parent=self.azimuth_y_axis_item)
                    lineitem.setPen(self.scene.axis_pen)

                    text = str((position - az_offset) * self.scene.azimuthscale // 4)
                    textitem = AzimuthScaleTextItem(text, value=position, parent=self.azimuth_y_axis_item)
                    textitem.setFont(self.scene.axis_font)
                    textitem.setBrush(self.scene.axis_color)
                    textitemwidth = textitem.boundingRect().width()
                    textitemheight = textitem.boundingRect().height()
                    if position == 4:
                        textitem.setPos(self.scene.elevationgraphicsareatopleft_x, y)

                        saved_width = textitemwidth
                        text = 'FT'
                        textitem = QtWidgets.QGraphicsSimpleTextItem(text, parent=self.azimuth_y_axis_item)
                        textitem.setFont(self.scene.axis_font)
                        textitem.setBrush(self.scene.axis_color)
                        textitemwidth = textitem.boundingRect().width()
                        textitemheight = textitem.boundingRect().height()
                        textitem.setPos(self.scene.elevationgraphicsareatopleft_x + saved_width - textitemwidth, y + textitemheight)
                    
                    elif position == -4:
                        textitem.setPos(self.scene.elevationgraphicsareatopleft_x, y - textitemheight)

                        saved_width = textitemwidth
                        text = 'FT'
                        textitem = QtWidgets.QGraphicsSimpleTextItem(text, parent=self.azimuth_y_axis_item)
                        textitem.setFont(self.scene.axis_font)
                        textitem.setBrush(self.scene.axis_color)
                        textitemwidth = textitem.boundingRect().width()
                        textitemheight = textitem.boundingRect().height()
                        textitem.setPos(self.scene.elevationgraphicsareatopleft_x + saved_width - textitemwidth, y - 2*textitemheight)
                    else:
                        textitem.setPos(self.scene.elevationgraphicsareatopleft_x, y - textitemheight / 2)
                    
            #self.azimuth_y_axis_item.setZValue(self.scene.axis_zvalue)

            self.addToGroup(self.azimuth_y_axis_item)
            
            #print self.azimuth_y_axis_item.filtersChildEvents()
            #self.addToGroup(self.azimuth_y_axis_item)
            #print self.azimuth_y_axis_item.filtersChildEvents()
            #print self.filtersChildEvents()

    #def mousePressEvent(self, event):
    #    print 'group kuuuuuuuuuuuuuuuuuuuuuuuuuuuk'

class RangeAxis(QtCore.QObject):
    
    def __init__(self, scene):
        super(RangeAxis, self).__init__()

        self.scene = scene

        #scene.addItem(self)
        
        self.elevation_x_axis_item = None
        self.azimuth_x_axis_item = None
        
        #self.setZValue(self.scene.axis_zvalue)
        self.create()


    def draw(self):
        self.create()


    def create(self):
        
        if self.elevation_x_axis_item and self.azimuth_x_axis_item:     # Either both are 1 or both are 0
            #self.removeFromGroup(self.elevation_x_axis_item)
            #self.removeFromGroup(self.azimuth_x_axis_item)
            
            self.scene.removeItem(self.elevation_x_axis_item)
            self.scene.removeItem(self.azimuth_x_axis_item)
            
            self.elevation_x_axis_item = None
            self.azimuth_x_axis_item = None

        if self.scene.rangescale:
        
            self.elevation_x_axis_item = QtWidgets.QGraphicsLineItem(self.scene.elevationrangeaxiszero_x, self.scene.elevationrangeaxis_y, self.scene.elevationrangeaxismax_x, self.scene.elevationrangeaxis_y)
            self.elevation_x_axis_item.setPen(self.scene.axis_pen)
            self.elevation_x_axis_item.setZValue(self.scene.axis_zvalue)

            az_offset = self.scene.az_offset
            delta_y = (self.scene.azimuthaxismax_y - self.scene.azimuthaxiszero_y) / 4
            y = self.scene.azimuthaxiszero_y + az_offset * delta_y

            self.azimuth_x_axis_item = QtWidgets.QGraphicsLineItem(self.scene.azimuthrangeaxiszero_x, y, self.scene.azimuthrangeaxismax_x, y)
            #self.azimuth_x_axis_item = QtGui.QGraphicsLineItem(self.scene.azimuthrangeaxiszero_x, self.scene.azimuthrangeaxis_y, self.scene.azimuthrangeaxismax_x, self.scene.azimuthrangeaxis_y)
            self.azimuth_x_axis_item.setPen(self.scene.axis_pen)
            self.azimuth_x_axis_item.setZValue(self.scene.axis_zvalue)

            if self.scene.rangescale == 1:
                numberoffullmarkings = 6
                markingtext = ['0', '0.2', '0.4', '0.6', '0.8', '1']
            elif self.scene.rangescale == 3:
                numberoffullmarkings = 4
                markingtext = ['0', '1', '2', '3']
            elif self.scene.rangescale == 5:
                numberoffullmarkings = 6
                markingtext = ['0', '1', '2', '3', '4', '5']
            elif self.scene.rangescale == 10:
                numberoffullmarkings = 6
                markingtext = ['0', '2', '4', '6', '8', '10']
            if self.scene.rangescale == 15:
                numberoffullmarkings = 6
                markingtext = ['0', '3', '6', '9', '12', '15']
            elif self.scene.rangescale == 20:
                numberoffullmarkings = 5
                markingtext = ['0', '5', '10', '15', '20']

            delta_x = (self.scene.elevationrangeaxismax_x - self.scene.elevationrangeaxiszero_x) / (numberoffullmarkings - 1)

            for c in range(numberoffullmarkings):
                x = self.scene.elevationrangeaxiszero_x + c * delta_x
                lineitem = QtWidgets.QGraphicsLineItem(x, self.scene.elevationrangeaxis_y + self.scene.axismarkinglength / 2, x, self.scene.elevationrangeaxis_y - self.scene.axismarkinglength / 2, parent=self.elevation_x_axis_item)
                lineitem.setPen(self.scene.axis_pen)
                #lineitem2 = QtGui.QGraphicsLineItem(x, self.scene.azimuthrangeaxis_y + self.scene.axismarkinglength / 2, x, self.scene.azimuthrangeaxis_y - self.scene.axismarkinglength / 2, parent=self.azimuth_x_axis_item)
                lineitem2 = QtWidgets.QGraphicsLineItem(x, y + self.scene.axismarkinglength / 2, x, y - self.scene.axismarkinglength / 2, parent=self.azimuth_x_axis_item)
                lineitem2.setPen(self.scene.axis_pen)

                textitem = QtWidgets.QGraphicsSimpleTextItem(markingtext[c], parent=self.elevation_x_axis_item)
                textitem.setFont(self.scene.axis_font)
                textitem.setBrush(self.scene.axis_color)
                textitemwidth = textitem.boundingRect().width()
                textitemheight = textitem.boundingRect().height()
                if c == len(markingtext) - 1:
                    textitem.setPos(x - textitemwidth, self.scene.elevationrangeaxis_y + self.scene.axismarkinglength / 2 + 4)
                else:
                    textitem.setPos(x - textitemwidth / 2.0, self.scene.elevationrangeaxis_y + self.scene.axismarkinglength / 2 + 4)

                textitem2 = QtWidgets.QGraphicsSimpleTextItem(markingtext[c], parent=self.azimuth_x_axis_item)
                textitem2.setFont(self.scene.axis_font)
                textitem2.setBrush(self.scene.axis_color)
                textitemwidth = textitem2.boundingRect().width()
                textitemheight = textitem2.boundingRect().height()
                if c == len(markingtext) - 1:
                    #textitem2.setPos(x - textitemwidth, self.scene.azimuthrangeaxis_y + self.scene.axismarkinglength / 2 + 4)
                    textitem2.setPos(x - textitemwidth, y + self.scene.axismarkinglength / 2 + 4)
                else:
                    #textitem2.setPos(x - textitemwidth / 2.0, self.scene.azimuthrangeaxis_y + self.scene.axismarkinglength / 2 + 4)
                    textitem2.setPos(x - textitemwidth / 2.0, y + self.scene.axismarkinglength / 2 + 4)

            if self.scene.rangescale == 1:
                numberofhalfmarkings = numberoffullmarkings - 1
                for c in range(numberofhalfmarkings):
                    x = self.scene.elevationrangeaxiszero_x + c * delta_x
                    line = QtWidgets.QGraphicsLineItem(x + delta_x / 2, self.scene.elevationrangeaxis_y + self.scene.axismarkinglength / 4, x + delta_x / 2, self.scene.elevationrangeaxis_y - self.scene.axismarkinglength / 4, parent=self.elevation_x_axis_item)
                    line.setPen(self.scene.axis_pen)
                    #line2 = QtGui.QGraphicsLineItem(x + delta_x / 2, self.scene.azimuthrangeaxis_y + self.scene.axismarkinglength / 4, x + delta_x / 2, self.scene.azimuthrangeaxis_y - self.scene.axismarkinglength / 4, parent=self.azimuth_x_axis_item)
                    line2 = QtWidgets.QGraphicsLineItem(x + delta_x / 2, y + self.scene.axismarkinglength / 4, x + delta_x / 2, y - self.scene.axismarkinglength / 4, parent=self.azimuth_x_axis_item)
                    line2.setPen(self.scene.axis_pen)
            
            self.elevation_x_axis_item.setZValue(self.scene.axis_zvalue)
            self.azimuth_x_axis_item.setZValue(self.scene.axis_zvalue)

            self.scene.addItem(self.elevation_x_axis_item)
            self.scene.addItem(self.azimuth_x_axis_item)

            #self.addToGroup(self.elevation_x_axis_item)
            #self.addToGroup(self.azimuth_x_axis_item)



#class WHIAxis(QtWidgets.QGraphicsItemGroup):
class WHIAxis(QtCore.QObject):
    
    def __init__(self, scene):
        super(WHIAxis, self).__init__()

        self.scene = scene

        #scene.addItem(self)
        
        self.x_axis_item = None
        self.y_axis_item = None
        
        #self.setZValue(self.scene.axis_zvalue)
        self.create()


    def draw(self):
        self.x_axis_item.setVisible(self.scene.whi_active)
        self.y_axis_item.setVisible(self.scene.whi_active)


    def create(self):
        self.x_axis_item = QtWidgets.QGraphicsLineItem(self.scene.whiaxiszero_x - self.scene.whiaxislength_x/2, self.scene.whiaxiszero_y, 
                                                   self.scene.whiaxiszero_x + self.scene.whiaxislength_x/2, self.scene.whiaxiszero_y)
        self.x_axis_item.setPen(self.scene.axis_pen)
        
        self.y_axis_item = QtWidgets.QGraphicsLineItem(self.scene.whiaxiszero_x, self.scene.whiaxiszero_y - self.scene.whiaxislength_y/2, 
                                                   self.scene.whiaxiszero_x, self.scene.whiaxiszero_y + self.scene.whiaxislength_y/2)
        self.y_axis_item.setPen(self.scene.axis_pen)
        
        
        marking_line_item = QtWidgets.QGraphicsLineItem(self.scene.whiaxiszero_x - self.scene.whiaxislength_x/2, self.scene.whiaxiszero_y - self.scene.whiaxismarkinglength/2, 
                                                   self.scene.whiaxiszero_x - self.scene.whiaxislength_x/2, self.scene.whiaxiszero_y + self.scene.whiaxismarkinglength/2, parent=self.x_axis_item)
        marking_line_item.setPen(self.scene.axis_pen)
        
        marking_line_item = QtWidgets.QGraphicsLineItem(self.scene.whiaxiszero_x - self.scene.whiaxislength_x/4, self.scene.whiaxiszero_y - self.scene.whiaxismarkinglength/2, 
                                                   self.scene.whiaxiszero_x - self.scene.whiaxislength_x/4, self.scene.whiaxiszero_y + self.scene.whiaxismarkinglength/2, parent=self.x_axis_item)
        marking_line_item.setPen(self.scene.axis_pen)
        
        marking_line_item = QtWidgets.QGraphicsLineItem(self.scene.whiaxiszero_x + self.scene.whiaxislength_x/2, self.scene.whiaxiszero_y - self.scene.whiaxismarkinglength/2, 
                                                   self.scene.whiaxiszero_x + self.scene.whiaxislength_x/2, self.scene.whiaxiszero_y + self.scene.whiaxismarkinglength/2, parent=self.x_axis_item)
        marking_line_item.setPen(self.scene.axis_pen)
        
        marking_line_item = QtWidgets.QGraphicsLineItem(self.scene.whiaxiszero_x + self.scene.whiaxislength_x/4, self.scene.whiaxiszero_y - self.scene.whiaxismarkinglength/2, 
                                                   self.scene.whiaxiszero_x + self.scene.whiaxislength_x/4, self.scene.whiaxiszero_y + self.scene.whiaxismarkinglength/2, parent=self.x_axis_item)
        marking_line_item.setPen(self.scene.axis_pen)
        
        
        
        marking_line_item = QtWidgets.QGraphicsLineItem(self.scene.whiaxiszero_x - self.scene.whiaxismarkinglength/2, self.scene.whiaxiszero_y - self.scene.whiaxislength_y/2, 
                                                   self.scene.whiaxiszero_x + self.scene.whiaxismarkinglength/2, self.scene.whiaxiszero_y - self.scene.whiaxislength_y/2, parent=self.x_axis_item)
        marking_line_item.setPen(self.scene.axis_pen)
        
        marking_line_item = QtWidgets.QGraphicsLineItem(self.scene.whiaxiszero_x - self.scene.whiaxismarkinglength/2, self.scene.whiaxiszero_y - self.scene.whiaxislength_y/4, 
                                                   self.scene.whiaxiszero_x + self.scene.whiaxismarkinglength/2, self.scene.whiaxiszero_y - self.scene.whiaxislength_y/4, parent=self.x_axis_item)
        marking_line_item.setPen(self.scene.axis_pen)
        
        marking_line_item = QtWidgets.QGraphicsLineItem(self.scene.whiaxiszero_x - self.scene.whiaxismarkinglength/2, self.scene.whiaxiszero_y + self.scene.whiaxislength_y/2, 
                                                   self.scene.whiaxiszero_x + self.scene.whiaxismarkinglength/2, self.scene.whiaxiszero_y + self.scene.whiaxislength_y/2, parent=self.x_axis_item)
        marking_line_item.setPen(self.scene.axis_pen)
        
        marking_line_item = QtWidgets.QGraphicsLineItem(self.scene.whiaxiszero_x - self.scene.whiaxismarkinglength/2, self.scene.whiaxiszero_y + self.scene.whiaxislength_y/4, 
                                                   self.scene.whiaxiszero_x + self.scene.whiaxismarkinglength/2, self.scene.whiaxiszero_y + self.scene.whiaxislength_y/4, parent=self.x_axis_item)
        marking_line_item.setPen(self.scene.axis_pen)



        textitem = QtWidgets.QGraphicsSimpleTextItem('-1000 ft', parent=self.x_axis_item)
        textitem.setFont(self.scene.axis_font)
        textitem.setBrush(self.scene.axis_color)
        textitemwidth = textitem.boundingRect().width()
        textitemheight = textitem.boundingRect().height()
        textitem.setPos(self.scene.whiaxiszero_x - self.scene.whiaxislength_x/2 - textitemwidth/2, self.scene.whiaxiszero_y + self.scene.whiaxismarkinglength / 2 + 4)
        
        textitem = QtWidgets.QGraphicsSimpleTextItem('+1000 ft', parent=self.x_axis_item)
        textitem.setFont(self.scene.axis_font)
        textitem.setBrush(self.scene.axis_color)
        textitemwidth = textitem.boundingRect().width()
        textitemheight = textitem.boundingRect().height()
        textitem.setPos(self.scene.whiaxiszero_x + self.scene.whiaxislength_x/2 - textitemwidth/2, self.scene.whiaxiszero_y + self.scene.whiaxismarkinglength / 2 + 4)


        textitem = QtWidgets.QGraphicsSimpleTextItem('-500 ft', parent=self.y_axis_item)
        textitem.setFont(self.scene.axis_font)
        textitem.setBrush(self.scene.axis_color)
        textitemwidth = textitem.boundingRect().width()
        textitemheight = textitem.boundingRect().height()
        textitem.setPos(self.scene.whiaxiszero_x - textitemwidth - self.scene.whiaxismarkinglength - 4.0, 
                        self.scene.whiaxiszero_y + self.scene.whiaxislength_y/2 - textitemheight/2)

        textitem = QtWidgets.QGraphicsSimpleTextItem('+500 ft', parent=self.y_axis_item)
        textitem.setFont(self.scene.axis_font)
        textitem.setBrush(self.scene.axis_color)
        textitemwidth = textitem.boundingRect().width()
        textitemheight = textitem.boundingRect().height()
        textitem.setPos(self.scene.whiaxiszero_x - textitemwidth - self.scene.whiaxismarkinglength - 4.0, 
                        self.scene.whiaxiszero_y - self.scene.whiaxislength_y/2 - textitemheight/2)


        self.x_axis_item.setZValue(self.scene.axis_zvalue)
        self.y_axis_item.setZValue(self.scene.axis_zvalue)

        self.scene.addItem(self.x_axis_item)
        self.scene.addItem(self.y_axis_item)

        #self.addToGroup(self.x_axis_item)
        #self.addToGroup(self.y_axis_item)
        
        self.draw()
        
    
#    whiaxislength_x = scenetotalheight / 8
#    whiaxislength_y = whiaxislength_x
#    whiaxiszero_x = whiaxislength_x * 1.5
#    whiaxiszero_y = whiaxislength_y * 0.66