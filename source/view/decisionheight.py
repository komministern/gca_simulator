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

import numpy as np

class DecisionHeight(QtWidgets.QGraphicsItemGroup):
    
    def __init__(self, scene):
        super(DecisionHeight, self).__init__(scene=scene)

        self.scene = scene

        self.scene.addItem(self)
        
        self.decisionheight_item = None
        
        self.glideslope = None
        self.decisionheight = None
        self.rangescale = None
        self.elevationscale = None
        
        self.setZValue(self.scene.decisionheight_zvalue)
        
        self.create()


    def draw(self):
        
        # If the decisionheight or rangescale or elevationscale or glideslope differs from the last creation, create new line item.
        if (self.scene.decisionheight != self.decisionheight) or (self.scene.rangescale != self.rangescale) or (self.scene.elevationscale != self.elevationscale) or (self.scene.glideslope != self.glideslope):
            self.create()


    def create(self):
        
        if self.decisionheight_item:

            self.scene.removeItem(self)

            self.removeFromGroup(self.decisionheight_item)
            self.decisionheight_item = None

            self.scene.addItem(self)
        
        if (self.scene.decisionheight != None) and self.scene.glideslope and self.scene.rangescale and self.scene.elevationscale and self.scene.touchdown_elevation_point:
        
            self.decisionheight = self.scene.decisionheight
            self.rangescale = self.scene.rangescale
            self.elevationscale = self.scene.elevationscale
            self.glideslope = self.scene.glideslope

            decisionheight_coordinate = np.array([(-self.decisionheight/3.2808399)/np.tan(self.glideslope*np.pi/180), 0.0, (self.decisionheight/3.2808399)])
            decisionheight_point = self.scene.getElevationPoint(decisionheight_coordinate)
            x = decisionheight_point.x()
            y = decisionheight_point.y()
            
            line = QtCore.QLineF(x - self.scene.decisionheight_length/2, y, x + self.scene.decisionheight_length/2, y)
            
            self.decisionheight_item = QtWidgets.QGraphicsLineItem(line)
            self.decisionheight_item.setPen(self.scene.decisionheight_pen)
            
            self.addToGroup(self.decisionheight_item)