
from PySide import QtGui, QtCore


class ElevationRunway(QtGui.QGraphicsItemGroup):
    
    def __init__(self, scene):
        super(ElevationRunway, self).__init__(scene=scene)
        
        self.elevation_runway_item = None
        
        self.setZValue(self.scene().runway_zvalue)
        
        self.create()


    def draw(self):
        self.create()
        self.setVisible(self.scene().connected)

        
        
    def create(self):
        
        if self.elevation_runway_item:
            
            self.removeFromGroup(self.elevation_runway_item)
            self.elevation_runway_item = None
        
        if self.scene().eor_elevation_point and self.scene().threshold_elevation_point:
            
            # Adjust the height in the eor point to have the same heiht as the threshold point.
            cheat_eor_elevation_point = QtCore.QPointF(self.scene().eor_elevation_point)
            cheat_eor_elevation_point.setY(self.scene().threshold_elevation_point.y())
            # This (above) is not correct, but it gives a nicer look.
        
            # Limit the drawing area leftwards
            if cheat_eor_elevation_point.x() < self.scene().elevationminrangegraphicsrange:
                cheat_eor_elevation_point.setX(self.scene().elevationminrangegraphicsrange)

            line = QtCore.QLineF(self.scene().threshold_elevation_point, cheat_eor_elevation_point)
            self.elevation_runway_item = QtGui.QGraphicsLineItem(line)
            self.elevation_runway_item.setPen(self.scene().runway_pen)
            
            textitem = QtGui.QGraphicsSimpleTextItem(self.scene().active_airport.runways[self.scene().active_runway]['name'], parent=self.elevation_runway_item)
            
            textitem.setFont(self.scene().textinfo_font)
            textitem.setBrush(self.scene().textinfo_brush)
            textitemwidth = textitem.boundingRect().width()
            textitemheight = textitem.boundingRect().height()
            textitem.setPos(self.scene().elevationgraphicsareatopleft_x, self.scene().elevationrangeaxis_y - textitemheight / 2)
            
            painterpath = QtGui.QPainterPath()
            painterpath.addEllipse(self.scene().threshold_elevation_point.x() - 3.0, self.scene().threshold_elevation_point.y(), 6.0, 20.0)
            painterpath.addEllipse(self.scene().threshold_elevation_point.x() - 3.0, self.scene().threshold_elevation_point.y() - 20.0, 6.0, 20.0)
        
            self.path_item = QtGui.QGraphicsPathItem(painterpath, parent=self.elevation_runway_item)
            self.path_item.setPen(self.scene().runway_pen)
            
            self.addToGroup(self.elevation_runway_item)
            
            
            
class AzimuthRunway(QtGui.QGraphicsItemGroup):
    
    def __init__(self, scene):
        super(AzimuthRunway, self).__init__(scene=scene)
        
        self.azimuth_runway_item = None
        
        self.setZValue(self.scene().runway_zvalue)
        
        self.create()


    def draw(self):
        
        self.create()
        self.setVisible(self.scene().connected)

        
        
    def create(self):
        
        if self.azimuth_runway_item:
            
            self.removeFromGroup(self.azimuth_runway_item)
            self.azimuth_runway_item = None
        
        if self.scene().eor_azimuth_point and self.scene().threshold_azimuth_point:

            modified_eor_azimuth_point = QtCore.QPointF(self.scene().eor_azimuth_point)
            if self.scene().eor_azimuth_point.x() < self.scene().azimuthminrangegraphicsrange:
                modified_eor_azimuth_point.setX(self.scene().azimuthminrangegraphicsrange)
        
            line = QtCore.QLineF(self.scene().threshold_azimuth_point, modified_eor_azimuth_point)
            self.azimuth_runway_item = QtGui.QGraphicsLineItem(line)
            self.azimuth_runway_item.setPen(self.scene().runway_pen)
        
            textitem = QtGui.QGraphicsSimpleTextItem(self.scene().active_airport.runways[self.scene().active_runway]['name'], parent=self.azimuth_runway_item)
            textitem.setFont(self.scene().textinfo_font)
            textitem.setBrush(self.scene().textinfo_brush)
            textitemwidth = textitem.boundingRect().width()
            textitemheight = textitem.boundingRect().height()

            az_offset = self.scene().az_offset
            delta_y = (self.scene().azimuthaxismax_y - self.scene().azimuthaxiszero_y) / 4

            textitem.setPos(self.scene().azimuthgraphicsareatopleft_x, self.scene().azimuthrangeaxis_y + az_offset * delta_y - textitemheight / 2)

            painterpath = QtGui.QPainterPath()
            painterpath.addEllipse(self.scene().threshold_azimuth_point.x() - 3.0, self.scene().threshold_azimuth_point.y(), 6.0, 20.0)
            painterpath.addEllipse(self.scene().threshold_azimuth_point.x() - 3.0, self.scene().threshold_azimuth_point.y() - 20.0, 6.0, 20.0)
        
            self.path_item = QtGui.QGraphicsPathItem(painterpath, parent=self.azimuth_runway_item)
            self.path_item.setPen(self.scene().runway_pen)
            
            self.addToGroup(self.azimuth_runway_item)

