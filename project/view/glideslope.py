


from PySide2 import QtCore, QtWidgets, QtGui

import numpy as np

#class GlideSlope(QtWidgets.QGraphicsItemGroup):
class GlideSlope(QtCore.QObject):
    
    def __init__(self, scene):
        super(GlideSlope, self).__init__()  #scene=scene)

        self.scene = scene

        #scene.addItem(self)

        
        self.glideslope_item = None
        
        self.glideslope = None
        self.rangescale = None
        self.elevationscale = None
        
        #self.setZValue(self.scene.glideslope_zvalue)
        
        self.create()


    def draw(self):
        
        # If the rangescale or elevationscale or glideslope differs from the last creation, create new line items.
        if (self.scene.rangescale != self.rangescale) or (self.scene.elevationscale != self.elevationscale) or (self.scene.glideslope != self.glideslope):
            self.create()

        
        
    def create(self):
        
        if self.glideslope_item:

            #print('removing glideslope_item')
            #print('before')
            #print(self.childItems())

            self.scene.removeItem(self.glideslope_item)
            self.glideslope_item = None

            #print('after')
            #print(self.childItems())
            #self.glideslope_item = None
        
        if self.scene.glideslope and self.scene.rangescale and self.scene.elevationscale and self.scene.touchdown_elevation_point:
        
            self.glideslope = self.scene.glideslope
            self.rangescale = self.scene.rangescale
            self.elevationscale = self.scene.elevationscale

            m_per_x_pixel = self.scene.rangescale*1852.0 / (self.scene.rangeaxismax_x - self.scene.rangeaxiszero_x)
            m_per_y_pixel = self.scene.elevationscale*0.3048 / (self.scene.elevationaxiszero_y - self.scene.elevationaxismax_y)

            glideslope_start_point = self.scene.touchdown_elevation_point
            glideslope_slope = np.tan(self.scene.glideslope*np.pi/180) * m_per_x_pixel / m_per_y_pixel
            glideslope_end_point = QtCore.QPointF(self.scene.rangeaxismax_x, glideslope_start_point.y() - glideslope_slope*(self.scene.rangeaxismax_x - glideslope_start_point.x()))
           
            # Keep glideslope line inside the elevation graphics area
            if glideslope_end_point.y() < self.scene.elevationgraphicsareatopleft_y:
                new_x = -1.0 * (self.scene.elevationgraphicsareatopleft_y - glideslope_start_point.y()) / glideslope_slope + glideslope_start_point.x()
                if new_x > self.scene.rangeaxismax_x:
                    new_x = self.scene.rangeaxismax_x
                
                delta_x = new_x - glideslope_start_point.x()
                glideslope_end_point = QtCore.QPointF(new_x, glideslope_start_point.y() - glideslope_slope*delta_x)

            line = QtCore.QLineF(glideslope_start_point, glideslope_end_point)
            self.glideslope_item = QtWidgets.QGraphicsLineItem(line)
            self.glideslope_item.setPen(self.scene.glideslope_pen)
            
            #self.addToGroup(self.glideslope_item)
        
            if self.scene.rangescale == 1:
                numberoffullmarkings = 6
            elif self.scene.rangescale == 3:
                numberoffullmarkings = 4
            elif self.scene.rangescale == 5:
                numberoffullmarkings = 6
            elif self.scene.rangescale == 10:
                numberoffullmarkings = 6
            if self.scene.rangescale == 15:
                numberoffullmarkings = 6
            elif self.scene.rangescale == 20:
                numberoffullmarkings = 5

            slope = (glideslope_end_point.y() - self.scene.touchdown_elevation_point.y()) / (glideslope_end_point.x() - self.scene.touchdown_elevation_point.x())
            delta_x = (self.scene.elevationrangeaxismax_x - self.scene.elevationrangeaxiszero_x) / (numberoffullmarkings - 1)
            delta_y = delta_x * slope

            for c in range(numberoffullmarkings):
                x = self.scene.elevationrangeaxiszero_x + c * delta_x
                y = self.scene.elevationrangeaxis_y + c * delta_y
                if y > self.scene.elevationgraphicsareatopleft_y:
                    lineitem = QtWidgets.QGraphicsLineItem(x, y + self.scene.glideslopemarkinglength / 2, x, y - self.scene.glideslopemarkinglength / 2, parent=self.glideslope_item)
                    lineitem.setPen(self.scene.glideslope_pen)
        
            self.glideslope_item.setZValue(self.scene.glideslope_zvalue)

            self.scene.addItem(self.glideslope_item)
