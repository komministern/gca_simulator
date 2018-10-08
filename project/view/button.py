#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    Copyright � 2016, 2017 Oscar Franz�n <oscarfranzen@yahoo.se>
#
#    This file is part of GCA Simulator.

from PySide import QtGui, QtCore


class Button(QtCore.QObject, QtGui.QGraphicsRectItem):

    pressed = QtCore.Signal(object)

    buttonnormalframewidth = 4
    buttonexpandedframewidth = 3


    def __init__(self, text, value=None):
        
        QtCore.QObject.__init__(self)
        QtGui.QGraphicsRectItem.__init__(self)

        self.value = value

        self.inverted = False
        self.hovered = False
        self.expanded = False

        self.text = text

        self.setAcceptHoverEvents(True)
        
        brush = QtGui.QBrush(QtCore.Qt.black)
        self.setBrush(brush)
        
        pen = QtGui.QPen(QtCore.Qt.black)
        pen.setWidth(4)
        self.setPen(pen)

        

        
    def setGeometry(self, x, y, width, height):
        
        self.setRect(x+self.buttonnormalframewidth, y+self.buttonnormalframewidth, width-2*self.buttonnormalframewidth, height-2*self.buttonnormalframewidth)
        
        font = QtGui.QFont("Helvetica", 10)
        
        lines = self.text.split('\n')
        if len(lines) == 1:
            self.textitem = QtGui.QGraphicsSimpleTextItem(lines[0], parent=self)
            self.textitem.setFont(font)
            self.textitem.setBrush(QtCore.Qt.yellow)
            wtext = (self.textitem.boundingRect().width())
            htext = (self.textitem.boundingRect().height())
            self.textitem.setPos(x+self.buttonnormalframewidth+(width-2*self.buttonnormalframewidth-wtext)/2, y+self.buttonnormalframewidth+(height-2*self.buttonnormalframewidth-htext)/2)

        elif len(lines) == 2:
            
            self.textitemtop = QtGui.QGraphicsSimpleTextItem(lines[0], parent=self)
            self.textitembottom = QtGui.QGraphicsSimpleTextItem(lines[1], parent=self)
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
            
            print 'ERROR!!!!!!!!!!'

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
            pen.setWidth(4)
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
            pen.setWidth(4)
            self.setPen(pen)
            for each in self.childItems():
                each.setBrush(QtGui.QBrush(QtCore.Qt.black))
        self.update()
        
    def hoverEnterEvent(self, event):
        self.hovered = True
        if self.inverted:
            pen = QtGui.QPen(QtCore.Qt.black)
            pen.setWidth(4)
            self.setPen(pen)
        else:
            if self.expanded:
                pen = QtGui.QPen(QtCore.Qt.yellow)
            else:
                pen = QtGui.QPen(QtCore.Qt.white)
            pen.setWidth(4)
            self.setPen(pen)
        
    def hoverLeaveEvent(self, event):
        self.hovered = False
        if self.inverted:
            pen = QtGui.QPen(QtCore.Qt.yellow)
            pen.setWidth(4)
            self.setPen(pen)
        else:
            if self.expanded:
                pen = QtGui.QPen(QtCore.Qt.yellow)
                pen.setWidth(3)
            else:
                pen = QtGui.QPen(QtCore.Qt.black)
                pen.setWidth(4)
            self.setPen(pen)
        
    def mousePressEvent(self, event):
        self.pressed.emit(self)
        
        
        
        #self.parentItem().setFocused()  # Buttons has no parents?!?
        
        
        
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
    
    def mousePressEvent(self, event):
        self.toggleExpanded()
        if self.expanded: 
            
            self.window.showWindow(self)

        else:
            self.window.hideWindow()
            
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
