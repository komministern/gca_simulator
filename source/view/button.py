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

class Button(QtCore.QObject, QtWidgets.QGraphicsRectItem):

    pressed = QtCore.Signal(object)

    #buttonnormalframewidth = 4
    #buttonexpandedframewidth = 3
    buttonnormalframewidth = 2
    buttonexpandedframewidth = 2


    def __init__(self, text, value=None, parent=None):
        
        QtCore.QObject.__init__(self)
        QtWidgets.QGraphicsRectItem.__init__(self)

        self.value = value

        self.inverted = False
        self.hovered = False
        self.expanded = False

        self.text = text

        self.setAcceptHoverEvents(True)
        
        brush = QtGui.QBrush(QtCore.Qt.black)
        self.setBrush(brush)
        
        pen = QtGui.QPen(QtCore.Qt.black)
        #pen.setWidth(4)
        pen.setWidth(2)
        self.setPen(pen)

        

        
    def setGeometry(self, x, y, width, height):
        
        self.setRect(x+self.buttonnormalframewidth, y+self.buttonnormalframewidth, width-2*self.buttonnormalframewidth, height-2*self.buttonnormalframewidth)
        
        font = QtGui.QFont("Helvetica", 10)
        font.setStretch(QtGui.QFont.Expanded)
        
        lines = self.text.split('\n')
        if len(lines) == 1:
            self.textitem = QtWidgets.QGraphicsSimpleTextItem(lines[0], parent=self)
            self.textitem.setFont(font)
            self.textitem.setBrush(QtCore.Qt.yellow)
            wtext = (self.textitem.boundingRect().width())
            htext = (self.textitem.boundingRect().height())
            self.textitem.setPos(x+self.buttonnormalframewidth+(width-2*self.buttonnormalframewidth-wtext)/2, y+self.buttonnormalframewidth+(height-2*self.buttonnormalframewidth-htext)/2)

        elif len(lines) == 2:
            
            self.textitemtop = QtWidgets.QGraphicsSimpleTextItem(lines[0], parent=self)
            self.textitembottom = QtWidgets.QGraphicsSimpleTextItem(lines[1], parent=self)
            self.textitemtop.setFont(font)
            self.textitemtop.setBrush(QtCore.Qt.yellow)
            self.textitembottom.setFont(font)
            self.textitembottom.setBrush(QtCore.Qt.yellow)

            wtexttop = (self.textitemtop.boundingRect().width())
            htexttop = (self.textitemtop.boundingRect().height())
            
            wtextbottom = (self.textitembottom.boundingRect().width())
            htextbottom = (self.textitembottom.boundingRect().height())

            self.textitemtop.setPos(x+self.buttonnormalframewidth+(width-2*self.buttonnormalframewidth-wtexttop)/2, y+self.buttonnormalframewidth+(height-2*self.buttonnormalframewidth-htexttop)/2-htexttop/2-1)
            self.textitembottom.setPos(x+self.buttonnormalframewidth+(width-2*self.buttonnormalframewidth-wtextbottom)/2, y+self.buttonnormalframewidth+(height-2*self.buttonnormalframewidth-htextbottom)/2+htextbottom/2+1)

        else:
            
            print('ERROR!!!!!!!!!!')

    def toggleExpanded(self):
        if self.expanded:
            self.expanded = False
            if self.hovered:
                pen = QtGui.QPen(QtCore.Qt.white)
            else:
                pen = QtGui.QPen(QtCore.Qt.black)
            pen.setWidth(4)
        else:
            self.expanded = True
            if self.hovered:
                pen = QtGui.QPen(QtCore.Qt.yellow)
                pen.setWidth(4)
            else:
                pen = QtGui.QPen(QtCore.Qt.yellow)
                pen.setWidth(3)
        self.setPen(pen)
        self.update()


    def setInverted(self, abool):
        if not abool == self.inverted:
            self.toggleInverted()

    def toggleInverted(self):
        if self.inverted:
            self.inverted = False
            brush = QtGui.QBrush(QtCore.Qt.black)
            self.setBrush(brush)
            if self.hovered:
                pen = QtGui.QPen(QtCore.Qt.white)
            else:
                pen = QtGui.QPen(QtCore.Qt.black)
            #pen.setWidth(4)
            pen.setWidth(2)
            self.setPen(pen)
            for each in self.childItems():
                each.setBrush(QtGui.QBrush(QtCore.Qt.yellow))
        else:
            self.inverted = True
            brush = QtGui.QBrush(QtCore.Qt.yellow)
            self.setBrush(brush)
            if self.hovered:
                pen = QtGui.QPen(QtCore.Qt.black)
            else:
                pen = QtGui.QPen(QtCore.Qt.yellow)
            #pen.setWidth(4)
            pen.setWidth(2)
            self.setPen(pen)
            for each in self.childItems():
                each.setBrush(QtGui.QBrush(QtCore.Qt.black))
        self.update()
        
    def hoverEnterEvent(self, event):
        self.hovered = True
        if self.inverted:
            pen = QtGui.QPen(QtCore.Qt.black)
            #pen.setWidth(4)
            pen.setWidth(3)
            self.setPen(pen)
        else:
            if self.expanded:
                pen = QtGui.QPen(QtCore.Qt.yellow)
            else:
                pen = QtGui.QPen(QtCore.Qt.white)
            #pen.setWidth(4)
            pen.setWidth(3)
            self.setPen(pen)
        
    def hoverLeaveEvent(self, event):
        self.hovered = False
        if self.inverted:
            pen = QtGui.QPen(QtCore.Qt.yellow)
            #pen.setWidth(4)
            pen.setWidth(2)
            self.setPen(pen)
        else:
            if self.expanded:
                pen = QtGui.QPen(QtCore.Qt.yellow)
                #pen.setWidth(3)
                pen.setWidth(2)
            else:
                pen = QtGui.QPen(QtCore.Qt.black)
                #pen.setWidth(4)
                pen.setWidth(2)
            self.setPen(pen)
        
    def mousePressEvent(self, event):
        
        if self.parentItem() and self.parentItem().parentItem():
            if not isinstance(self, ExpandingButton) and not self.expanded:
                self.parentItem().parentItem().setFocused()
        self.pressed.emit(self)
        
        
        
class InvertingButton(Button):
    
    def __init__(self, text, value=None, exclusivegroup=None):
        super(InvertingButton, self).__init__(text, value)

        self.exclusivegroup = exclusivegroup
        if self.exclusivegroup != None:
            self.exclusivegroup.append(self)


    def resetExclusiveGroupButtons(self):
        if self.exclusivegroup:
            for each in self.exclusivegroup:
                if each.inverted:
                    each.toggleInverted()


    def mousePressEvent(self, event):
        
        if self.exclusivegroup:

            if not self.inverted:
                self.toggleInverted()
        
                for each in self.exclusivegroup:
                    if each.inverted and each != self:
                        each.toggleInverted()

        else:

            self.toggleInverted()
            
        Button.mousePressEvent(self, event)


class ExpandingButton(Button):
    
    def __init__(self, text, window):
        super(ExpandingButton, self).__init__(text)
        
        self.window = window

        self.temporary_window = None

    def mousePressEvent(self, event):
        
        self.toggleExpanded()
        
        if self.expanded: 
            
            if not self.window.isHidden():
                
                # We can only end up here if the window that is supposed to be opened, already is open.
                # This should only be possible with the view.password_entry_window. We shall assume that
                # this is the case, and proceed with destroying this window before showing it anew.

                self.window.activatingbutton.toggleExpanded()
                self.window.activatingbutton = None
                self.window.hideWindow()
                #button.hoverLeaveEvent(None)    # Just to get rid of some non esthetic things

            self.window.showWindow(self)

        else:

            if self.temporary_window:

                self.temporary_window.hideWindow()
                self.temporary_window = None
            else:

                self.window.hideWindow()
            
        Button.mousePressEvent(self, event)
        


class ExpandingWidgetButton(Button):
    
    def __init__(self, text, widget):
        super(ExpandingWidgetButton, self).__init__(text)
        
        self.widget = widget

        self.temporary_window = None

    def mousePressEvent(self, event):
        
        self.toggleExpanded()
        
        if self.expanded: 
            
            self.widget.show()

        else:

            self.widget.close()
            
        Button.mousePressEvent(self, event)



class FlashingButton(Button):
    
    def __init__(self, text, value=None):
        super(FlashingButton, self).__init__(text, value)
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.toggleInverted)

    def mousePressEvent(self, event):
        self.toggleInverted()
        self.timer.start(100)
            
        Button.mousePressEvent(self, event)



class PendingButton(Button):
    
    def __init__(self, text, value=None):
        super(PendingButton, self).__init__(text, value)
        self.pending = False
        self.pending_color = QtGui.QColor(104, 104, 0)
        
    def mousePressEvent(self, event):
        #self.togglePending()
            
        Button.mousePressEvent(self, event)

    def setPending(self, abool):
        if not abool == self.pending:
            self.togglePending()
        

    def togglePending(self):

        if self.pending:
            self.pending = False
            brush = QtGui.QBrush(QtCore.Qt.black)
            self.setBrush(brush)
            if self.hovered:
                pen = QtGui.QPen(QtCore.Qt.white)
            else:
                pen = QtGui.QPen(QtCore.Qt.black)
            pen.setWidth(4)
            self.setPen(pen)
            for each in self.childItems():
                each.setBrush(QtGui.QBrush(QtCore.Qt.yellow))
        else:
            self.pending = True
            brush = QtGui.QBrush(self.pending_color)
            self.setBrush(brush)
            if self.hovered:
                pen = QtGui.QPen(QtCore.Qt.black)
            else:
                pen = QtGui.QPen(self.pending_color)
            pen.setWidth(4)
            self.setPen(pen)
            for each in self.childItems():
                each.setBrush(QtGui.QBrush(QtCore.Qt.black))
        self.update()
