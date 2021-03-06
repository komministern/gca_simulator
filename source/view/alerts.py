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

import functools
#from PySide import QtGui, QtCore
from PySide2 import QtWidgets, QtCore, QtGui


class AlertsField(QtCore.QObject):
    
    # QGraphicsItemGroup seems ideal for this, but a bug concerning propagation of
    # signals from scene to the member items of the group made this difficult.
    # This works and will do.
    # The field is not movable, but could easily be made so. Should it?
    #

    sound_alarm_on = QtCore.Signal()
    sound_alarm_off = QtCore.Signal()
    
    def __init__(self, scene):
        super(AlertsField, self).__init__()
        self.scene = scene
        self.frame_item = None
        self.alerts = []


    def addAlert(self, text, critical=False, delay=0.0):
        if delay == 0.0:
            if len(self.alerts) == 0:
                self.alerts.append(NonClickableAlert('ALERT', self, scene=self.scene))

            #if unicode(' ' + text + ' ') not in [each.toPlainText() for each in self.alerts]:
            if ' ' + text + ' ' not in [each.toPlainText() for each in self.alerts]:
                if not critical:
                    self.alerts.append(Alert(text, self, scene=self.scene))
                else:
                    self.alerts.append(CriticalAlert(text, self, scene=self.scene))
                    self.sound_alarm_on.emit()
                self.draw()
        elif delay > 0.0:
            laterAlert = functools.partial(self.addAlert, text, critical=critical)
            self.timer = QtCore.QTimer.singleShot(delay, laterAlert)


    def clickOnAllAlerts(self):
        for each in self.alerts[1:]:
            if not each.acknowledged:
                each.acknowledged = True
                each.revertText()
            elif each.acknowledged:
                each.obsolete = True
        self.draw()


    def draw(self):
        if self.frame_item:
            self.scene.removeItem(self.frame_item)
            del self.frame_item
        self.frame_item = None
        
        updated_alerts = []
        
        for each in self.alerts:
            if not each.obsolete:
                updated_alerts.append(each)
            self.scene.removeItem(each)
        
        if len(updated_alerts) > 1:
            y = 0.0
            largest_width = 0.0
            for each in updated_alerts:
                self.scene.addItem(each)
                each.setPos(self.scene.alerts_field_centre_x - each.width/2.0, self.scene.alerts_field_top_y + y)
                largest_width = max(largest_width, each.width)
                y += each.height

            # Some kind of minimal width perhaps? Or even better. See to it that all alert texts are of some decent minimum length (and maximum)
            self.frame_item = QtWidgets.QGraphicsRectItem(self.scene.alerts_field_centre_x - largest_width/2.0 - self.scene.alerts_frame_margin, self.scene.alerts_field_top_y - self.scene.alerts_frame_margin, 
                                                      largest_width + self.scene.alerts_frame_margin*2, y + self.scene.alerts_frame_margin*2)#, scene=self.scene)
            
            self.scene.addItem(self.frame_item)

            self.frame_item.setPen(self.scene.alerts_field_pen)
            self.alerts = updated_alerts
        else:
            self.alerts = []
        
        # Are there any critical alerts still unacknowledged?
        if not (False in [each.acknowledged for each in self.alerts]):
            self.sound_alarm_off.emit()


class Alert(QtWidgets.QGraphicsTextItem):
        
    def __init__(self, text, field, scene):
        super(Alert, self).__init__(' ' + text + ' ')   #, scene=scene)

        scene.addItem(self)

        self.field = field
        self.setFont(self.scene().alerts_font)
        self.setZValue(self.scene().alerts_zvalue)
        self.document().setDocumentMargin(0.5)
        self.width = self.boundingRect().width()
        self.height = self.boundingRect().height()
        self.setDefaultTextColor(self.scene().alerts_color)
        self.acknowledged = True
        self.obsolete = False

    def mousePressEvent(self, event):
        self.obsolete = True
        self.field.draw()


class CriticalAlert(Alert):
    def __init__(self, text, field, scene):
        super(CriticalAlert, self).__init__(text, field, scene=scene)
        self.acknowledged = False
        self.invertText()
        # Start sound alarm through some Signal perhaps!?!
        
    def invertText(self):
        cursor = self.textCursor()
        format = QtGui.QTextCharFormat()
        format.setBackground(QtGui.QBrush(self.scene().alerts_color))
        format.setForeground(QtGui.QBrush(QtCore.Qt.black))
        cursor.setPosition(0)
        cursor.movePosition(QtGui.QTextCursor.EndOfLine, QtGui.QTextCursor.KeepAnchor, 1)
        cursor.mergeCharFormat(format)
        
    def revertText(self):
        cursor = self.textCursor()
        format = QtGui.QTextCharFormat()
        format.setBackground(QtGui.QBrush(QtCore.Qt.black))
        format.setForeground(QtGui.QBrush(self.scene().alerts_color))
        cursor.setPosition(0)
        cursor.movePosition(QtGui.QTextCursor.EndOfLine, QtGui.QTextCursor.KeepAnchor, 1)
        cursor.mergeCharFormat(format)
        
    def mousePressEvent(self, event):
        if not self.acknowledged:
            self.acknowledged = True
            self.revertText()
        else:
            self.obsolete = True
        self.field.draw()

class NonClickableAlert(Alert):
    def __init__(self, text, field, scene):
        super(NonClickableAlert, self).__init__(text, field, scene=scene)
        
    def mousePressEvent(self, event):
        pass