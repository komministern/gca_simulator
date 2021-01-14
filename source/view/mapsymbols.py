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

class MapSymbols(QtCore.QObject):
    
    def __init__(self, scene):
        super(MapSymbols, self).__init__()

        #scene.addItem(self)

        self.scene = scene

        
        self.mapsymbols_item = None
        self.create()





    def draw(self):
        self.create()
        self.mapsymbols_item.setVisible(self.scene.map_active)
    
    def create(self):
        if self.mapsymbols_item:
            #self.removeFromGroup(self.mapsymbols_item)

            self.scene.removeItem(self.mapsymbols_item)

            self.mapsymbols_item = None
        
        if self.scene.rangescale:

            self.mapsymbols_item = QtWidgets.QGraphicsItemGroup()

            top_triangle_point = QtCore.QPointF(self.scene.range_to_scenexcoord(-3*1852.0), self.scene.azimuth_to_sceneycoord(0.0))
            left_triangle_point = top_triangle_point + QtCore.QPointF(-8.0, 8.0)
            right_triangle_point = top_triangle_point + QtCore.QPointF(8.0, 8.0)

            triangle_polygon = QtGui.QPolygonF()
            triangle_polygon.append(top_triangle_point)
            triangle_polygon.append(left_triangle_point)
            triangle_polygon.append(right_triangle_point)

            self.triangle_item = QtWidgets.QGraphicsPolygonItem(triangle_polygon, parent=self.mapsymbols_item)

            
            self.triangle_brush = QtGui.QBrush(self.scene.axis_color)
            self.triangle_pen = QtGui.QPen(self.scene.axis_color)
            self.triangle_pen.setWidth(1.0)

            self.triangle_item.setPen(self.triangle_pen)
            self.triangle_item.setBrush(self.triangle_brush)

            self.mapsymbols_item.addToGroup(self.triangle_item)


            self.marker_pen = QtGui.QPen(QtCore.Qt.red)
            self.marker_pen.setWidth(2.0)

            self.light_marker_pen = QtGui.QPen(QtCore.Qt.red)
            self.light_marker_pen.setWidth(1.0)


            i_height = 12.0
            i_width = 4.0
            x = self.scene.range_to_scenexcoord(-0.5*1852.0)
            delta_y = 34.0
            self.i_item = QtWidgets.QGraphicsItemGroup()

            for i in range(-2, 3):
                y = self.scene.azimuth_to_sceneycoord(i * delta_y)
                
                lineitem = QtWidgets.QGraphicsLineItem(x, y-i_height / 2.0, x, y+i_height / 2.0, parent=self.i_item)
                lineitem.setPen(self.light_marker_pen)
                lineitem = QtWidgets.QGraphicsLineItem(x-i_width / 2.0, y-i_height / 2.0, x+i_width / 2.0, y-i_height / 2.0, parent=self.i_item)
                lineitem.setPen(self.light_marker_pen)
                lineitem = QtWidgets.QGraphicsLineItem(x-i_width / 2.0, y+i_height / 2.0, x+i_width / 2.0, y+i_height / 2.0, parent=self.i_item)
                lineitem.setPen(self.light_marker_pen)

            

            self.mapsymbols_item.addToGroup(self.i_item)

            self.mapsymbols_item.setZValue(self.scene.mapsymbols_zvalue)

            self.scene.addItem(self.mapsymbols_item)

            #self.addToGroup(self.mapsymbols_item)

