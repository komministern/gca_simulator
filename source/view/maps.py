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

from PySide import QtGui, QtCore
#import time

class Maps(QtGui.QGraphicsItemGroup):
    
    def __init__(self, scene):
        super(Maps, self).__init__(scene=scene)
        
        #self.textinfo_item = None
        
        self.setZValue(self.scene().textinfo_zvalue)
        self.create()


    def draw(self):
        
        # Draw Time
        self.timetextinfo_item.setText(time.strftime('TIME: ' + '%H:%M:%S', time.gmtime()))
        
        # Draw RWY
        if self.scene().active_airport != None and self.scene().active_runway != None:
            try:
                rwy_direction_text = str(self.scene().active_airport.runways[self.scene().active_runway]['true'])
            except Exception:
                rwy_direction_text = '---'
        else:
            rwy_direction_text = ''
        self.rwytextinfo_item.setText('RWY: ' + rwy_direction_text)

        # Draw DH
        if self.scene().decisionheight:
            dh_text = str(self.scene().decisionheight)
        else:
            dh_text = ''
        self.dhtextinfo_item.setText('DH: ' + dh_text)
        
        # Draw GS
        if self.scene().glideslope:
            gs_text = str(self.scene().glideslope)
        else:
            gs_text = ''
        self.gstextinfo_item.setText('GS: ' + gs_text)

    def create(self):

        self.gstextinfo_item = QtGui.QGraphicsSimpleTextItem('')
        self.gstextinfo_item.setFont(self.scene().textinfo_font)
        self.gstextinfo_item.setBrush(self.scene().textinfo_brush)
        self.gstextinfo_item.setPos(self.scene().textgraphicsareatopleft_x + 1.0*self.scene().textgraphicsareawidth/8, self.scene().textgraphicsareatopleft_y)

        self.rwytextinfo_item = QtGui.QGraphicsSimpleTextItem('', parent=self.gstextinfo_item)
        self.rwytextinfo_item.setFont(self.scene().textinfo_font)
        self.rwytextinfo_item.setBrush(self.scene().textinfo_brush)
        self.rwytextinfo_item.setPos(1.0*self.scene().textgraphicsareawidth/8, 0.0)

        self.dhtextinfo_item = QtGui.QGraphicsSimpleTextItem('', parent=self.gstextinfo_item)
        self.dhtextinfo_item.setFont(self.scene().textinfo_font)
        self.dhtextinfo_item.setBrush(self.scene().textinfo_brush)
        self.dhtextinfo_item.setPos(2.0*self.scene().textgraphicsareawidth/8, 0.0)

        self.timetextinfo_item = QtGui.QGraphicsSimpleTextItem('', parent=self.gstextinfo_item)
        self.timetextinfo_item.setFont(self.scene().textinfo_font)
        self.timetextinfo_item.setBrush(self.scene().textinfo_brush)
        self.timetextinfo_item.setPos(3.0*self.scene().textgraphicsareawidth/8, 0.0)
            
        self.addToGroup(self.gstextinfo_item)
        
        self.draw()
        
        
        
        
        
        
        
        
        

        
        
    def drawMapSymbols(self):
        
        if self.mapsymbols_item:
            self.removeItem(self.mapsymbols_item)
            del self.mapsymbols_item
            self.mapsymbols_item = None
            
        if self.map_active:
            
            self.mapsymbols_item = QtGui.QGraphicsItemGroup(parent=None, scene=self)
            
            lineitem = QtGui.QGraphicsLineItem(0.0, 0.0, 100.0, 100.0, parent=self.mapsymbols_item)
            lineitem.setPen(self.axis_pen)