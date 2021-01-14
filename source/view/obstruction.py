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

import random
import numpy as np

class Obstruction(QtWidgets.QGraphicsItemGroup):
    
    def __init__(self, scene):
        super(Obstruction, self).__init__()

        self.scene = scene

        self.scene.addItem(self)

        self.setZValue(self.scene.obstruction_zvalue)
        
        self.obstruction_item = None

        self.random = random.Random()

        #self.calculate()
        #self.create()


    def calculate(self):

        seed = int( self.scene.active_airport.runways[self.scene.active_runway]['thr_lon'] * 10000 )
        self.random.seed(seed)

        self.dx = 1.0 / 6 * 1852                            # One sixth of a nautical mile (m)
        self.dy = 100.0 / 3.2808399                         # One hundred feet (m)

        self.upper_angle_limit_for_obs = 2.0 * np.pi / 180  # (radians)
        
        self.min_obs_start_distance = 1.0 * 1852
        self.max_obs_start_distance = 3.0 * 1852

        self.min_obs_end_distance = 4.0 * 1852
        self.max_obs_end_distance = 6.0 * 1852

        self.n_min_obs_start_distance = self.n_dx(self.min_obs_start_distance)
        self.n_max_obs_start_distance = self.n_dx(self.max_obs_start_distance)
        
        self.n_min_obs_end_distance = self.n_dx(self.min_obs_end_distance)
        self.n_max_obs_end_distance = self.n_dx(self.max_obs_end_distance)



        self.n_obs_start_distance = self.random.randint(self.n_min_obs_start_distance, self.n_max_obs_start_distance)
        self.n_obs_end_distance = self.random.randint(self.n_min_obs_end_distance, self.n_max_obs_end_distance)



        self.n_min_obs_start_height = 1
        self.n_max_obs_start_height = self.n_limiting_height(self.n_obs_start_distance * self.dx)

        self.n_min_obs_end_height = self.n_limiting_height(self.n_obs_end_distance * self.dx) // 2
        self.n_max_obs_end_height = self.n_limiting_height(self.n_obs_end_distance * self.dx)



        self.n_obs_start_height = self.random.randint(self.n_min_obs_start_height, self.n_max_obs_start_height)
        self.n_obs_end_height = self.random.randint(self.n_min_obs_end_height, self.n_max_obs_end_height)


    
    def n_dx(self, x):
        return int(round(x/self.dx))

    def n_dy(self, y):
        return int(round(y/self.dy))

    def limiting_height(self, distance):
        return np.tan(self.upper_angle_limit_for_obs) * distance
    
    def n_limiting_height(self, distance):
        return int(self.limiting_height(distance) / self.dy)


    def draw(self):
        #self.calculate()
        self.create()
        self.setVisible(self.scene.obs_active)

        #print self.scene.active_airport
        #if self.scene.active_airport != None:
        #    print int( self.scene.active_airport.runways[self.scene.active_runway]['thr_lon'] * 10000 )
    

    def create(self):
        if self.obstruction_item:

            self.scene.removeItem(self)

            self.removeFromGroup(self.obstruction_item)

            self.obstruction_item = None
        
            self.scene.addItem(self)

        if self.scene.rangescale and self.scene.active_airport != None:

            self.calculate()

            self.obstruction_item = QtWidgets.QGraphicsItemGroup()
  
            n_x = self.n_obs_start_distance
            n_y = self.n_obs_start_height

            n_x_end = self.n_obs_end_distance
            n_y_end = self.n_obs_end_height

            while( (n_x_end - n_x) > 0 ):
            
                topleft = QtCore.QPointF(self.scene.range_to_scenexcoord(-n_x * self.dx), self.scene.altitude_to_sceneycoord(n_y * self.dy))
                bottomright = QtCore.QPointF(self.scene.range_to_scenexcoord(-(n_x + 1) * self.dx), self.scene.altitude_to_sceneycoord(0.0))
                if topleft.x() < self.scene.elevationgraphicsareabottomright_x:
                    rect = QtCore.QRectF(topleft, bottomright)
                    rectitem = QtWidgets.QGraphicsRectItem(rect, parent=self.obstruction_item)
                    rectitem.setPen(self.scene.obstruction_pen)
                    rectitem.setBrush(self.scene.obstruction_brush)

                p_increase = 1.0 * (n_y_end - n_y) / (n_x_end - n_x)
                if (self.random.random() < p_increase) and ( (n_y + 1) * self.dy < self.limiting_height((n_x + 1) * self.dx) ):
                    n_y += 1
                
                n_x += 1

            self.addToGroup(self.obstruction_item)