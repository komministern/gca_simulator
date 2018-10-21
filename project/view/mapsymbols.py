
from PySide import QtCore, QtGui

class MapSymbols(QtGui.QGraphicsItemGroup):
    
    def __init__(self, scene):
        super(MapSymbols, self).__init__(scene=scene)
        self.setZValue(self.scene().mapsymbols_zvalue)
        self.mapsymbols_item = None
        self.create()
    
    def draw(self):
        self.create()
        self.setVisible(self.scene().map_active)
    
    def create(self):
        if self.mapsymbols_item:
            self.removeFromGroup(self.mapsymbols_item)
            self.mapsymbols_item = None
        
        if self.scene().rangescale:

            self.mapsymbols_item = QtGui.QGraphicsItemGroup()

            top_triangle_point = QtCore.QPointF(self.scene().range_to_scenexcoord(-3*1852.0), self.scene().azimuth_to_sceneycoord(0.0))
            left_triangle_point = top_triangle_point + QtCore.QPointF(-5.0, 10.0)
            right_triangle_point = top_triangle_point + QtCore.QPointF(5.0, 10.0)

            triangle_polygon = QtGui.QPolygonF()
            triangle_polygon.append(top_triangle_point)
            triangle_polygon.append(left_triangle_point)
            triangle_polygon.append(right_triangle_point)

            self.triangle_item = QtGui.QGraphicsPolygonItem(triangle_polygon, parent=self.mapsymbols_item)

            
            self.triangle_brush = QtGui.QBrush(self.scene().axis_color)
            self.triangle_pen = QtGui.QPen(self.scene().axis_color)
            self.triangle_pen.setWidth(1.0)

            self.triangle_item.setPen(self.triangle_pen)
            self.triangle_item.setBrush(self.triangle_brush)

            self.mapsymbols_item.addToGroup(self.triangle_item)

            self.marker_pen = QtGui.QPen(QtCore.Qt.red)
            self.marker_pen.setWidth(2.0)

            self.light_marker_pen = QtGui.QPen(QtCore.Qt.red)
            self.light_marker_pen.setWidth(1.0)

            x = self.scene().range_to_scenexcoord(-0.5*1852.0)
            y = self.scene().azimuth_to_sceneycoord(0.0)

            self.lineitem = QtGui.QGraphicsLineItem(x, y + 8.0, x, y - 7.0, parent=self.mapsymbols_item)
            self.lineitem.setPen(self.marker_pen)

            for dy in [8, 6, 4, 2, 0, -2, -4, -6, -8]:
                lineitem = QtGui.QGraphicsLineItem(x - 2.5, y + dy, x + 2.5, y + dy, parent=self.lineitem)
                lineitem.setPen(self.light_marker_pen)



            self.addToGroup(self.mapsymbols_item)

