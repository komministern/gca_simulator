
from PySide import QtGui, QtCore


class ElevationAxis(QtGui.QGraphicsItemGroup):
    
    def __init__(self, scene):
        super(ElevationAxis, self).__init__(scene=scene)
        
        self.elevation_y_axis_item = None
        self.setZValue(self.scene().axis_zvalue)
        self.create()


    def draw(self):
        
        self.create()


    def create(self):
        
        if self.elevation_y_axis_item:
            self.removeFromGroup(self.elevation_y_axis_item)
            self.elevation_y_axis_item = None

        if self.scene().elevationscale and self.scene().rangescale:

            line = QtCore.QLineF(self.scene().elevationaxis_x, self.scene().elevationaxismax_y, self.scene().elevationaxis_x, self.scene().elevationaxismin_y)
            self.elevation_y_axis_item = QtGui.QGraphicsLineItem(line)
            self.elevation_y_axis_item.setPen(self.scene().axis_pen)
        
            x = self.scene().elevationaxis_x
            delta_y = (self.scene().elevationaxismax_y - self.scene().elevationaxiszero_y) / 4
            for c in range(1, 5):

                y = self.scene().elevationaxiszero_y + c * delta_y

                lineitem = QtGui.QGraphicsLineItem(x - self.scene().axismarkinglength / 2,  y, x + self.scene().axismarkinglength / 2, y, parent=self.elevation_y_axis_item)
                lineitem.setPen(self.scene().axis_pen)

                text = str(c * self.scene().elevationscale / 4)
                textitem = QtGui.QGraphicsSimpleTextItem(text, parent=self.elevation_y_axis_item)
                textitem.setFont(self.scene().axis_font)
                textitem.setBrush(self.scene().axis_color)
                textitemwidth = textitem.boundingRect().width()
                textitemheight = textitem.boundingRect().height()
                if c == 4:
                    textitem.setPos(self.scene().elevationgraphicsareatopleft_x, y)
                else:
                    textitem.setPos(self.scene().elevationgraphicsareatopleft_x, y - textitemheight / 2)

            y = self.scene().elevationaxiszero_y - delta_y / 2
            lineitem = QtGui.QGraphicsLineItem(x - self.scene().axismarkinglength / 2,  y, x + self.scene().axismarkinglength / 2, y, parent=self.elevation_y_axis_item)
            lineitem.setPen(self.scene().axis_pen)

            text = str(-1 * self.scene().elevationscale / 8)
            textitem = QtGui.QGraphicsSimpleTextItem(text, parent=self.elevation_y_axis_item)
            textitem.setFont(self.scene().axis_font)
            textitem.setBrush(self.scene().axis_color)
            textitemwidth = textitem.boundingRect().width()
            textitemheight = textitem.boundingRect().height()
            textitem.setPos(0.0, y - textitemheight)

            self.addToGroup(self.elevation_y_axis_item)



class AzimuthAxis(QtGui.QGraphicsItemGroup):
    
    def __init__(self, scene):
        super(AzimuthAxis, self).__init__(scene=scene)
        
        self.azimuth_y_axis_item = None
        self.setZValue(self.scene().axis_zvalue)
        self.create()


    def draw(self):
        
        self.create()


    def create(self):
        
        if self.azimuth_y_axis_item:
            self.removeFromGroup(self.azimuth_y_axis_item)
            self.azimuth_y_axis_item = None

        if self.scene().azimuthscale and self.scene().rangescale:

            line = QtCore.QLineF(self.scene().azimuthaxis_x, self.scene().azimuthaxismax_y, self.scene().azimuthaxis_x, self.scene().azimuthaxismin_y)
            self.azimuth_y_axis_item = QtGui.QGraphicsLineItem(line)
            self.azimuth_y_axis_item.setPen(self.scene().axis_pen)

            x = self.scene().azimuthaxis_x
            delta_y = (self.scene().azimuthaxismax_y - self.scene().azimuthaxiszero_y) / 4

            for c in range(-4, 5):

                y = self.scene().azimuthaxiszero_y + c * delta_y
                if c != 0:
                    lineitem = QtGui.QGraphicsLineItem(x - self.scene().axismarkinglength / 2,  y, x + self.scene().axismarkinglength / 2, y, parent=self.azimuth_y_axis_item)
                    lineitem.setPen(self.scene().axis_pen)

                    text = str(c * self.scene().azimuthscale / 4)
                    textitem = QtGui.QGraphicsSimpleTextItem(text, parent=self.azimuth_y_axis_item)
                    textitem.setFont(self.scene().axis_font)
                    textitem.setBrush(self.scene().axis_color)
                    textitemwidth = textitem.boundingRect().width()
                    textitemheight = textitem.boundingRect().height()
                    if c == 4:
                        textitem.setPos(self.scene().elevationgraphicsareatopleft_x, y)
                    elif c == -4:
                        textitem.setPos(self.scene().elevationgraphicsareatopleft_x, y - textitemheight)
                    else:
                        textitem.setPos(self.scene().elevationgraphicsareatopleft_x, y - textitemheight / 2)
                    
            self.addToGroup(self.azimuth_y_axis_item)



class RangeAxis(QtGui.QGraphicsItemGroup):
    
    def __init__(self, scene):
        super(RangeAxis, self).__init__(scene=scene)
        
        self.elevation_x_axis_item = None
        self.azimuth_x_axis_item = None
        
        self.setZValue(self.scene().axis_zvalue)
        self.create()


    def draw(self):
        self.create()


    def create(self):
        
        if self.elevation_x_axis_item and self.azimuth_x_axis_item:     # Either both are 1 or both are 0
            self.removeFromGroup(self.elevation_x_axis_item)
            self.removeFromGroup(self.azimuth_x_axis_item)
            self.elevation_x_axis_item = None
            self.azimuth_x_axis_item = None

        if self.scene().rangescale:
        
            self.elevation_x_axis_item = QtGui.QGraphicsLineItem(self.scene().elevationrangeaxiszero_x, self.scene().elevationrangeaxis_y, self.scene().elevationrangeaxismax_x, self.scene().elevationrangeaxis_y)
            self.elevation_x_axis_item.setPen(self.scene().axis_pen)
            self.elevation_x_axis_item.setZValue(self.scene().axis_zvalue)

            self.azimuth_x_axis_item = QtGui.QGraphicsLineItem(self.scene().azimuthrangeaxiszero_x, self.scene().azimuthrangeaxis_y, self.scene().azimuthrangeaxismax_x, self.scene().azimuthrangeaxis_y)
            self.azimuth_x_axis_item.setPen(self.scene().axis_pen)
            self.azimuth_x_axis_item.setZValue(self.scene().axis_zvalue)

            if self.scene().rangescale == 1:
                numberoffullmarkings = 6
                markingtext = ['0', '0.2', '0.4', '0.6', '0.8', '1']
            elif self.scene().rangescale == 3:
                numberoffullmarkings = 4
                markingtext = ['0', '1', '2', '3']
            elif self.scene().rangescale == 5:
                numberoffullmarkings = 6
                markingtext = ['0', '1', '2', '3', '4', '5']
            elif self.scene().rangescale == 10:
                numberoffullmarkings = 6
                markingtext = ['0', '2', '4', '6', '8', '10']
            if self.scene().rangescale == 15:
                numberoffullmarkings = 6
                markingtext = ['0', '3', '6', '9', '12', '15']
            elif self.scene().rangescale == 20:
                numberoffullmarkings = 5
                markingtext = ['0', '5', '10', '15', '20']

            delta_x = (self.scene().elevationrangeaxismax_x - self.scene().elevationrangeaxiszero_x) / (numberoffullmarkings - 1)

            for c in range(numberoffullmarkings):
                x = self.scene().elevationrangeaxiszero_x + c * delta_x
                lineitem = QtGui.QGraphicsLineItem(x, self.scene().elevationrangeaxis_y + self.scene().axismarkinglength / 2, x, self.scene().elevationrangeaxis_y - self.scene().axismarkinglength / 2, parent=self.elevation_x_axis_item)
                lineitem.setPen(self.scene().axis_pen)
                lineitem2 = QtGui.QGraphicsLineItem(x, self.scene().azimuthrangeaxis_y + self.scene().axismarkinglength / 2, x, self.scene().azimuthrangeaxis_y - self.scene().axismarkinglength / 2, parent=self.azimuth_x_axis_item)
                lineitem2.setPen(self.scene().axis_pen)

                textitem = QtGui.QGraphicsSimpleTextItem(markingtext[c], parent=self.elevation_x_axis_item)
                textitem.setFont(self.scene().axis_font)
                textitem.setBrush(self.scene().axis_color)
                textitemwidth = textitem.boundingRect().width()
                textitemheight = textitem.boundingRect().height()
                if c == len(markingtext) - 1:
                    textitem.setPos(x - textitemwidth, self.scene().elevationrangeaxis_y + self.scene().axismarkinglength / 2 + 4)
                else:
                    textitem.setPos(x - textitemwidth / 2.0, self.scene().elevationrangeaxis_y + self.scene().axismarkinglength / 2 + 4)

                textitem2 = QtGui.QGraphicsSimpleTextItem(markingtext[c], parent=self.azimuth_x_axis_item)
                textitem2.setFont(self.scene().axis_font)
                textitem2.setBrush(self.scene().axis_color)
                textitemwidth = textitem2.boundingRect().width()
                textitemheight = textitem2.boundingRect().height()
                if c == len(markingtext) - 1:
                    textitem2.setPos(x - textitemwidth, self.scene().azimuthrangeaxis_y + self.scene().axismarkinglength / 2 + 4)
                else:
                    textitem2.setPos(x - textitemwidth / 2.0, self.scene().azimuthrangeaxis_y + self.scene().axismarkinglength / 2 + 4)

            if self.scene().rangescale == 1:
                numberofhalfmarkings = numberoffullmarkings - 1
                for c in range(numberofhalfmarkings):
                    x = self.scene().elevationrangeaxiszero_x + c * delta_x
                    line = QtGui.QGraphicsLineItem(x + delta_x / 2, self.scene().elevationrangeaxis_y + self.scene().axismarkinglength / 4, x + delta_x / 2, self.scene().elevationrangeaxis_y - self.scene().axismarkinglength / 4, parent=self.elevation_x_axis_item)
                    line.setPen(self.scene().axis_pen)
                    line2 = QtGui.QGraphicsLineItem(x + delta_x / 2, self.scene().azimuthrangeaxis_y + self.scene().axismarkinglength / 4, x + delta_x / 2, self.scene().azimuthrangeaxis_y - self.scene().axismarkinglength / 4, parent=self.azimuth_x_axis_item)
                    line2.setPen(self.scene().axis_pen)
                    
            self.addToGroup(self.elevation_x_axis_item)
            self.addToGroup(self.azimuth_x_axis_item)



class WHIAxis(QtGui.QGraphicsItemGroup):
    
    def __init__(self, scene):
        super(WHIAxis, self).__init__(scene=scene)
        
        self.x_axis_item = None
        self.y_axis_item = None
        
        self.setZValue(self.scene().axis_zvalue)
        self.create()


    def draw(self):
        self.setVisible(self.scene().whi_active)


    def create(self):
        self.x_axis_item = QtGui.QGraphicsLineItem(self.scene().whiaxiszero_x - self.scene().whiaxislength_x/2, self.scene().whiaxiszero_y, 
                                                   self.scene().whiaxiszero_x + self.scene().whiaxislength_x/2, self.scene().whiaxiszero_y)
        self.x_axis_item.setPen(self.scene().axis_pen)
        
        self.y_axis_item = QtGui.QGraphicsLineItem(self.scene().whiaxiszero_x, self.scene().whiaxiszero_y - self.scene().whiaxislength_y/2, 
                                                   self.scene().whiaxiszero_x, self.scene().whiaxiszero_y + self.scene().whiaxislength_y/2)
        self.y_axis_item.setPen(self.scene().axis_pen)
        
        
        marking_line_item = QtGui.QGraphicsLineItem(self.scene().whiaxiszero_x - self.scene().whiaxislength_x/2, self.scene().whiaxiszero_y - self.scene().whiaxismarkinglength/2, 
                                                   self.scene().whiaxiszero_x - self.scene().whiaxislength_x/2, self.scene().whiaxiszero_y + self.scene().whiaxismarkinglength/2, parent=self.x_axis_item)
        marking_line_item.setPen(self.scene().axis_pen)
        
        marking_line_item = QtGui.QGraphicsLineItem(self.scene().whiaxiszero_x - self.scene().whiaxislength_x/4, self.scene().whiaxiszero_y - self.scene().whiaxismarkinglength/2, 
                                                   self.scene().whiaxiszero_x - self.scene().whiaxislength_x/4, self.scene().whiaxiszero_y + self.scene().whiaxismarkinglength/2, parent=self.x_axis_item)
        marking_line_item.setPen(self.scene().axis_pen)
        
        marking_line_item = QtGui.QGraphicsLineItem(self.scene().whiaxiszero_x + self.scene().whiaxislength_x/2, self.scene().whiaxiszero_y - self.scene().whiaxismarkinglength/2, 
                                                   self.scene().whiaxiszero_x + self.scene().whiaxislength_x/2, self.scene().whiaxiszero_y + self.scene().whiaxismarkinglength/2, parent=self.x_axis_item)
        marking_line_item.setPen(self.scene().axis_pen)
        
        marking_line_item = QtGui.QGraphicsLineItem(self.scene().whiaxiszero_x + self.scene().whiaxislength_x/4, self.scene().whiaxiszero_y - self.scene().whiaxismarkinglength/2, 
                                                   self.scene().whiaxiszero_x + self.scene().whiaxislength_x/4, self.scene().whiaxiszero_y + self.scene().whiaxismarkinglength/2, parent=self.x_axis_item)
        marking_line_item.setPen(self.scene().axis_pen)
        
        
        
        marking_line_item = QtGui.QGraphicsLineItem(self.scene().whiaxiszero_x - self.scene().whiaxismarkinglength/2, self.scene().whiaxiszero_y - self.scene().whiaxislength_y/2, 
                                                   self.scene().whiaxiszero_x + self.scene().whiaxismarkinglength/2, self.scene().whiaxiszero_y - self.scene().whiaxislength_y/2, parent=self.x_axis_item)
        marking_line_item.setPen(self.scene().axis_pen)
        
        marking_line_item = QtGui.QGraphicsLineItem(self.scene().whiaxiszero_x - self.scene().whiaxismarkinglength/2, self.scene().whiaxiszero_y - self.scene().whiaxislength_y/4, 
                                                   self.scene().whiaxiszero_x + self.scene().whiaxismarkinglength/2, self.scene().whiaxiszero_y - self.scene().whiaxislength_y/4, parent=self.x_axis_item)
        marking_line_item.setPen(self.scene().axis_pen)
        
        marking_line_item = QtGui.QGraphicsLineItem(self.scene().whiaxiszero_x - self.scene().whiaxismarkinglength/2, self.scene().whiaxiszero_y + self.scene().whiaxislength_y/2, 
                                                   self.scene().whiaxiszero_x + self.scene().whiaxismarkinglength/2, self.scene().whiaxiszero_y + self.scene().whiaxislength_y/2, parent=self.x_axis_item)
        marking_line_item.setPen(self.scene().axis_pen)
        
        marking_line_item = QtGui.QGraphicsLineItem(self.scene().whiaxiszero_x - self.scene().whiaxismarkinglength/2, self.scene().whiaxiszero_y + self.scene().whiaxislength_y/4, 
                                                   self.scene().whiaxiszero_x + self.scene().whiaxismarkinglength/2, self.scene().whiaxiszero_y + self.scene().whiaxislength_y/4, parent=self.x_axis_item)
        marking_line_item.setPen(self.scene().axis_pen)



        textitem = QtGui.QGraphicsSimpleTextItem('-1000 ft', parent=self.x_axis_item)
        textitem.setFont(self.scene().axis_font)
        textitem.setBrush(self.scene().axis_color)
        textitemwidth = textitem.boundingRect().width()
        textitemheight = textitem.boundingRect().height()
        textitem.setPos(self.scene().whiaxiszero_x - self.scene().whiaxislength_x/2 - textitemwidth/2, self.scene().whiaxiszero_y + self.scene().whiaxismarkinglength / 2 + 4)
        
        textitem = QtGui.QGraphicsSimpleTextItem('+1000 ft', parent=self.x_axis_item)
        textitem.setFont(self.scene().axis_font)
        textitem.setBrush(self.scene().axis_color)
        textitemwidth = textitem.boundingRect().width()
        textitemheight = textitem.boundingRect().height()
        textitem.setPos(self.scene().whiaxiszero_x + self.scene().whiaxislength_x/2 - textitemwidth/2, self.scene().whiaxiszero_y + self.scene().whiaxismarkinglength / 2 + 4)


        textitem = QtGui.QGraphicsSimpleTextItem('-500 ft', parent=self.y_axis_item)
        textitem.setFont(self.scene().axis_font)
        textitem.setBrush(self.scene().axis_color)
        textitemwidth = textitem.boundingRect().width()
        textitemheight = textitem.boundingRect().height()
        textitem.setPos(self.scene().whiaxiszero_x - textitemwidth - self.scene().whiaxismarkinglength - 4.0, 
                        self.scene().whiaxiszero_y + self.scene().whiaxislength_y/2 - textitemheight/2)

        textitem = QtGui.QGraphicsSimpleTextItem('+500 ft', parent=self.y_axis_item)
        textitem.setFont(self.scene().axis_font)
        textitem.setBrush(self.scene().axis_color)
        textitemwidth = textitem.boundingRect().width()
        textitemheight = textitem.boundingRect().height()
        textitem.setPos(self.scene().whiaxiszero_x - textitemwidth - self.scene().whiaxismarkinglength - 4.0, 
                        self.scene().whiaxiszero_y - self.scene().whiaxislength_y/2 - textitemheight/2)



        self.addToGroup(self.x_axis_item)
        self.addToGroup(self.y_axis_item)
        
        self.draw()
        
    
#    whiaxislength_x = scenetotalheight / 8
#    whiaxislength_y = whiaxislength_x
#    whiaxiszero_x = whiaxislength_x * 1.5
#    whiaxiszero_y = whiaxislength_y * 0.66