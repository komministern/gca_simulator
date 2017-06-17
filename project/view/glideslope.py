


from PySide import QtGui, QtCore
import numpy as np

class GlideSlope(QtGui.QGraphicsItemGroup):
    
    def __init__(self, scene):
        super(GlideSlope, self).__init__(scene=scene)
        
        self.glideslope_item = None
        
        self.glideslope = None
        self.rangescale = None
        self.elevationscale = None
        
        self.setZValue(self.scene().glideslope_zvalue)
        
        self.create()


    def draw(self):
        
        # If the rangescale or elevationscale or glideslope differs from the last creation, create new line items.
        if (self.scene().rangescale != self.rangescale) or (self.scene().elevationscale != self.elevationscale) or (self.scene().glideslope != self.glideslope):
            self.create()

        
        
    def create(self):
        
        if self.glideslope_item:
            self.removeFromGroup(self.glideslope_item)
            self.glideslope_item = None
        
        if self.scene().glideslope and self.scene().rangescale and self.scene().elevationscale and self.scene().touchdown_elevation_point:
        
            self.glideslope = self.scene().glideslope
            self.rangescale = self.scene().rangescale
            self.elevationscale = self.scene().elevationscale

            glideslope_start_point = self.scene().touchdown_elevation_point
            
            glideslope_end_coordinate = np.array([-1852.0*self.rangescale, 0.0, np.tan(self.glideslope*np.pi/180)*1852.0*self.rangescale])
            glideslope_end_point = self.scene().getElevationPoint(glideslope_end_coordinate)
            line = QtCore.QLineF(glideslope_start_point, glideslope_end_point)
            
            self.glideslope_item = QtGui.QGraphicsLineItem(line)
            self.glideslope_item.setPen(self.scene().glideslope_pen)
            
            self.addToGroup(self.glideslope_item)
        
            if self.scene().rangescale == 1:
                numberoffullmarkings = 6
            elif self.scene().rangescale == 3:
                numberoffullmarkings = 4
            elif self.scene().rangescale == 5:
                numberoffullmarkings = 6
            elif self.scene().rangescale == 10:
                numberoffullmarkings = 6
            if self.scene().rangescale == 15:
                numberoffullmarkings = 6
            elif self.scene().rangescale == 20:
                numberoffullmarkings = 5

            slope = (glideslope_end_point.y() - self.scene().touchdown_elevation_point.y()) / (glideslope_end_point.x() - self.scene().touchdown_elevation_point.x())
            delta_x = (self.scene().elevationrangeaxismax_x - self.scene().elevationrangeaxiszero_x) / (numberoffullmarkings - 1)
            delta_y = delta_x * slope

            for c in range(numberoffullmarkings):
                x = self.scene().elevationrangeaxiszero_x + c * delta_x
                y = self.scene().elevationrangeaxis_y + c * delta_y
                lineitem = QtGui.QGraphicsLineItem(x, y + self.scene().glideslopemarkinglength / 2, x, y - self.scene().glideslopemarkinglength / 2, parent=self.glideslope_item)
                lineitem.setPen(self.scene().glideslope_pen)
        
        
