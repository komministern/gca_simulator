
from PySide2 import QtCore, QtWidgets, QtGui

class ElevationGCA(QtWidgets.QGraphicsItemGroup):
    
    def __init__(self, scene):
        super(ElevationGCA, self).__init__()

        self.scene = scene

        self.scene.addItem(self)

        self.elevation_gca_item = None
        self.setZValue(self.scene.gca_zvalue)
        self.create()

    def draw(self):
        self.create()
        self.setVisible(self.scene.radarcover_active and self.scene.connected)

    def create(self):
        if self.elevation_gca_item:

            self.scene.removeItem(self)

            self.removeFromGroup(self.elevation_gca_item)
            
            self.elevation_gca_item = None

            self.scene.addItem(self)

        if self.scene.gca_elevation_point:
            rect = QtCore.QRectF(self.scene.gca_elevation_point.x()-7.5, self.scene.gca_elevation_point.y()-10.0, 15.0, 10.0)
            self.elevation_gca_item = QtWidgets.QGraphicsRectItem(rect)
            self.elevation_gca_item.setBrush(self.scene.gca_brush)
            
            self.addToGroup(self.elevation_gca_item)


class AzimuthGCA(QtWidgets.QGraphicsItemGroup):
    
    def __init__(self, scene):
        super(AzimuthGCA, self).__init__()

        self.scene = scene

        self.scene.addItem(self)

        self.azimuth_gca_item = None
        self.setZValue(self.scene.gca_zvalue)
        self.create()

    def draw(self):
        self.create()
        self.setVisible(self.scene.radarcover_active and self.scene.connected)

    def create(self):
        if self.azimuth_gca_item:

            self.scene.removeItem(self)

            self.removeFromGroup(self.azimuth_gca_item)

            self.azimuth_gca_item = None

            self.scene.addItem(self)

        if self.scene.gca_azimuth_point:
            rect = QtCore.QRectF(self.scene.gca_azimuth_point.x()-7.5, self.scene.gca_azimuth_point.y()-5.0, 15.0, 10.0)
            self.azimuth_gca_item = QtWidgets.QGraphicsRectItem(rect)
            self.azimuth_gca_item.setBrush(self.scene.gca_brush)
            
            self.addToGroup(self.azimuth_gca_item)
