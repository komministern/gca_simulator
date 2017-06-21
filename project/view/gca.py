
from PySide import QtGui, QtCore

class ElevationGCA(QtGui.QGraphicsItemGroup):
    
    def __init__(self, scene):
        super(ElevationGCA, self).__init__(scene=scene)
        self.elevation_gca_item = None
        self.setZValue(self.scene().gca_zvalue)
        self.create()

    def draw(self):
        self.create()
        self.setVisible(self.scene().radarcover_active and self.scene().connected)

    def create(self):
        if self.elevation_gca_item:
            self.removeFromGroup(self.elevation_gca_item)
            self.elevation_gca_item = None

        if self.scene().gca_elevation_point:
            rect = QtCore.QRectF(self.scene().gca_elevation_point.x()-7.5, self.scene().gca_elevation_point.y()-10.0, 15.0, 10.0)
            self.elevation_gca_item = QtGui.QGraphicsRectItem(rect)
            self.elevation_gca_item.setBrush(self.scene().gca_brush)
            
            self.addToGroup(self.elevation_gca_item)


class AzimuthGCA(QtGui.QGraphicsItemGroup):
    
    def __init__(self, scene):
        super(AzimuthGCA, self).__init__(scene=scene)
        self.azimuth_gca_item = None
        self.setZValue(self.scene().gca_zvalue)
        self.create()

    def draw(self):
        self.create()
        self.setVisible(self.scene().radarcover_active and self.scene().connected)

    def create(self):
        if self.azimuth_gca_item:
            self.removeFromGroup(self.azimuth_gca_item)
            self.azimuth_gca_item = None

        if self.scene().gca_azimuth_point:
            rect = QtCore.QRectF(self.scene().gca_azimuth_point.x()-7.5, self.scene().gca_azimuth_point.y()-5.0, 15.0, 10.0)
            self.azimuth_gca_item = QtGui.QGraphicsRectItem(rect)
            self.azimuth_gca_item.setBrush(self.scene().gca_brush)
            
            self.addToGroup(self.azimuth_gca_item)
