#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    Copyright © 2016, 2017 Oscar Franzén <oscarfranzen@yahoo.se>
#
#    This file is part of GCA Simulator.


from PySide import QtGui, QtCore
import time
from scene import MyScene


class WindowTopBorder(QtCore.QObject, QtGui.QGraphicsRectItem):

    windowleftxcoordinate = MyScene.buttonwindowareatopleft_x
    windowwidth = MyScene.buttonwindowareawidth

    windowframethickness = 3
    windowusablewidth = windowwidth - 2*windowframethickness
    
    borderthickness = 26
    
    closerectside = 18
    crossthickness = 2
    
    window_gets_shown = QtCore.Signal()
    window_gets_hidden = QtCore.Signal()
    window_gets_focus = QtCore.Signal()
    window_loses_focus = QtCore.Signal()

    
    def __init__(self, text):   #, update_when_made_visible=False):
        
        
        #super(WindowTopBorder, self).__init__()
        QtCore.QObject.__init__(self)
        QtGui.QGraphicsRectItem.__init__(self)
        
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        
        self.setRect(self.windowleftxcoordinate + self.windowframethickness, 
        self.windowframethickness, self.windowusablewidth, self.borderthickness)
        
        pen = QtGui.QPen()
        pen.setWidth(self.windowframethickness)
        pen.setColor(QtCore.Qt.lightGray)
        
        brush = QtGui.QBrush(QtCore.Qt.lightGray)
        self.setBrush(brush)
        self.setPen(pen)

        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)

        self.setAcceptHoverEvents(True)
        
        #self.update_when_made_visible = update_when_made_visible


        # The following section should be solved differently (see the updateTopBorderText method further down)

        font = QtGui.QFont("Helvetica", 10)
        font.setBold(True)
        self.textitem = QtGui.QGraphicsSimpleTextItem(text, parent=self)
            
        self.textitem.setFont(font)
        self.textitem.setBrush(QtCore.Qt.black)
            
        textwidth = int(self.textitem.boundingRect().width())
        textheight = int(self.textitem.boundingRect().height())
        
        topborderrect = self.rect()
        winx = topborderrect.x()
        winy = topborderrect.y()
        winwidth = topborderrect.width()
        winheight = topborderrect.height()
        
        self.textitem.setPos(winx+(winwidth-textwidth)/2, winy+(winheight-textheight)/2)

        # ................

        #self.textitem = None
        #self.updateTopBorderText(text)
        
        d = (winheight-self.closerectside)/2
        self.closeRect = QtGui.QGraphicsRectItem(winx+winwidth-self.closerectside-d, winy+d, self.closerectside, self.closerectside, parent=self)
        
        crosscenter = self.closeRect.rect().center()
        xcenter = crosscenter.x()
        ycenter = crosscenter.y()
        
        c = self.closerectside/4
        
        self.crossline1 = QtGui.QGraphicsLineItem(xcenter-c, ycenter-c, xcenter+c, ycenter+c, parent=self)
        self.crossline2 = QtGui.QGraphicsLineItem(xcenter-c, ycenter+c, xcenter+c, ycenter-c, parent=self)
        pen = QtGui.QPen(QtCore.Qt.black)
        pen.setWidth(self.crossthickness)
        self.crossline1.setPen(pen)
        self.crossline2.setPen(pen)

        self.hideWindow()
        
#        self.initial_focus_item = None


    def updateTopBorderText(self, text):
        
        if self.textitem != None:
            temp_brush = self.textitem.brush()
            self.textitem.setParentItem(None)   # This line is important, as....
            del self.textitem           # this one does not alone remove the item from the scene??? (And/or the parent)
        
        font = QtGui.QFont("Helvetica", 10)     # This font should be taken directly from the scene instead!!!
        font.setBold(True)
        
        self.textitem = QtGui.QGraphicsSimpleTextItem(text, parent=self)
            
        self.textitem.setFont(font)
        self.textitem.setBrush(temp_brush)
            
        textwidth = int(self.textitem.boundingRect().width())
        textheight = int(self.textitem.boundingRect().height())
        
        topborderrect = self.rect()
        winx = topborderrect.x()
        winy = topborderrect.y()
        winwidth = topborderrect.width()
        winheight = topborderrect.height()
        
        self.textitem.setPos(winx+(winwidth-textwidth)/2, winy+(winheight-textheight)/2)


    def isHidden(self):
        return not self.isEnabled()     # Hidden and (not enabled) goes together in this application


    def hideWindow(self):
        self.setUnFocused()
        self.setEnabled(False)
        self.setOpacity(0.0)
        self.setZValue(0.0)
        self.window_gets_hidden.emit()
    
    def showWindow(self, button=None):
        self.activatingbutton = button
        self.setFocused()
        self.setEnabled(True)
        self.setOpacity(1.0) 
        self.setFocused()
        self.window_gets_shown.emit()

        # This is most special!!! If the window area is InputWindowArea, the text in the top border always contains
        # the UTC time of the time of this methods execution. The last 8 chars is removed and replaced with correct time.
        if type(self.childItems()[0]) is InputWindowArea:
            temp_text = self.textitem.text()
            time_text = time.strftime('%H:%M:%S', time.gmtime())
            new_text = temp_text[0:-8] + time_text
            self.updateTopBorderText(new_text)


#    def setInitialFocusItem(self, item):
#        self.initial_focus_item = item


    def setFocused(self):
        self.scene().unFocusAllWindowTopBorders()
        
        self.setZValue(self.scene().getNewZVal())
        self.setBrush(QtCore.Qt.darkCyan)
        
        pen = QtGui.QPen()
        pen.setWidth(self.windowframethickness)
        pen.setColor(QtCore.Qt.darkCyan)
        self.setPen(pen)
        
        self.textitem.setBrush(QtCore.Qt.white)
        
        pen = QtGui.QPen()
        pen.setWidth(self.crossthickness)
        pen.setColor(QtCore.Qt.white)
        self.crossline1.setPen(pen)
        self.crossline2.setPen(pen)
        
#        if self.initial_focus_item != None:
#            self.initial_focus_item.setFocus()

        self.window_gets_focus.emit()
        

        
    def setUnFocused(self):
        
        self.setBrush(QtCore.Qt.lightGray)
        pen = QtGui.QPen()
        pen.setWidth(self.windowframethickness)
        pen.setColor(QtCore.Qt.lightGray)
        self.setPen(pen)
        
        self.textitem.setBrush(QtCore.Qt.black)

        pen = QtGui.QPen()
        pen.setWidth(self.crossthickness)
        pen.setColor(QtCore.Qt.black)
        self.crossline1.setPen(pen)
        self.crossline2.setPen(pen)
        
        self.window_loses_focus.emit()


    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemPositionChange:
            value.setX(0.0)
            if value.y() < 0:
                value.setY(0.0)
            # The value 761.0 is taken directly (quite ugly) from the mainwindowarea after it beeing created and moved
            # to the bottom of the screen. Horrific.
            
            #if value.y() > 761.0 - self.boundingRect().height() - self.childrenBoundingRect().height() + self.windowframethickness:
            #    value.setY(761.0 - self.boundingRect().height() - self.childrenBoundingRect().height() + self.windowframethickness)
            if value.y() > 838.0 - self.boundingRect().height() - self.childrenBoundingRect().height() + self.windowframethickness:
                value.setY(838.0 - self.boundingRect().height() - self.childrenBoundingRect().height() + self.windowframethickness)

        return super(WindowTopBorder, self).itemChange(change, value)  # <<<<< Must return the result !!!

    def mousePressEvent(self, event):
        
        if self.closeRect.rect().contains(event.pos()):
            
            if self.activatingbutton:
                self.activatingbutton.toggleExpanded()
                self.activatingbutton = None
            self.hideWindow()
        else:
        
            self.setFocused()
        


class WindowArea(QtCore.QObject, QtGui.QGraphicsRectItem):
    
    windowheight = MyScene.scenetotalheight
    windowleftxcoordinate = MyScene.buttonwindowareatopleft_x
    windowwidth = MyScene.buttonwindowareawidth

    distance = 5    # ...between buttons
    
    windowframethickness = 3
    windowusablewidth = windowwidth - 2*windowframethickness
    
    buttontwowidth = (windowusablewidth - 3*distance) / 2
    buttonthreewidth = (windowusablewidth - 4*distance) / 3
    buttonfourwidth = (windowusablewidth - 5*distance) / 4
    buttonfivewidth = (windowusablewidth - 6*distance) / 5
    
#    buttonhalfheight = buttonfourwidth / 2
#    buttonfullheight = buttonfourwidth

    buttonhalfheight = buttonfivewidth / 2
    buttonfullheight = buttonfivewidth

    textrowheight = 24

    lineseparatorthickness = 2
    lineseparatorheight = distance


    def __init__(self):
        
        QtCore.QObject.__init__(self)
        QtGui.QGraphicsRectItem.__init__(self)
        

        self.setRect(self.windowleftxcoordinate + self.windowframethickness, 
                     self.windowframethickness, self.windowusablewidth, 800)

        pen = QtGui.QPen()
        pen.setWidth(self.windowframethickness)
        pen.setColor(QtCore.Qt.white)
        self.setPen(pen)
        brush = QtGui.QBrush(QtCore.Qt.darkBlue)
        self.setBrush(brush)

        self.ycursor = self.windowframethickness
        self.xcursor = self.windowleftxcoordinate + self.windowframethickness + self.distance

        self.setAcceptHoverEvents(True)

    def mousePressEvent(self, event):
        if self.parentItem():
            self.parentItem().setFocused()


    def setFocused(self):
        if self.parentItem():
            self.parentItem().setFocused()


    def attachTo(self, top):
        self.setPos(self.x(), top.y()+top.boundingRect().height()-self.windowframethickness)
        self.setParentItem(top)
        self.setFlags(QtGui.QGraphicsItem.ItemStacksBehindParent)


    def newTextRow(self, text):
        self.presentbuttonheight = self.textrowheight
        textitem = QtGui.QGraphicsSimpleTextItem(text, parent=self)
        font = QtGui.QFont("Helvetica", 10)
        textitem.setFont(font)
        textitem.setBrush(QtCore.Qt.yellow)
        wtext = int(textitem.boundingRect().width())
        htext = int(textitem.boundingRect().height())
        textitem.setPos(self.xcursor+(self.windowusablewidth-wtext)/2, self.ycursor+self.distance)

    def newWhiteLineSeparator(self):
        self.presentbuttonheight = self.lineseparatorheight
        pen = QtGui.QPen()
        pen.setWidth(self.lineseparatorthickness)
        pen.setColor(QtCore.Qt.white)
        
        line = QtGui.QGraphicsLineItem(self.windowleftxcoordinate+2*self.lineseparatorthickness, self.ycursor+self.distance, self.windowleftxcoordinate+self.windowwidth-2*self.lineseparatorthickness, self.ycursor+self.distance)
        line.setPen(pen)
        line.setParentItem(self)
    
    def newHalfButtonRow(self, nx):
        self.ycursor += self.distance
        self.presentbuttonheight = self.buttonhalfheight
        #self.xcursor = self.windowleftxcoordinate + self.windowframethickness + self.distance
        if nx == 2:
            self.presentbuttonwidth = self.buttontwowidth
        elif nx == 3:
            self.presentbuttonwidth = self.buttonthreewidth
        elif nx == 4:
            self.presentbuttonwidth = self.buttonfourwidth
        elif nx == 5:
            self.presentbuttonwidth = self.buttonfivewidth
        else:
            print 'ERROR!!!!'

    def endRow(self):
        self.ycursor += self.presentbuttonheight
        self.xcursor = self.windowleftxcoordinate + self.windowframethickness + self.distance
    
    def newFullButtonRow(self, nx):
        self.ycursor += self.distance
        if nx == 5:
            self.presentbuttonheight = self.buttonfivewidth     #self.buttonfullheight      FOR GOOD LOOKS!
        else:
            self.presentbuttonheight = self.buttonfullheight
        self.xcursor = self.windowleftxcoordinate + self.windowframethickness + self.distance
        if nx == 2:
            self.presentbuttinwidth = self.buttontwowidth
        elif nx == 3:
            self.presentbuttonwidth = self.buttonthreewidth
        elif nx == 4:
            self.presentbuttonwidth = self.buttonfourwidth
        elif nx == 5:
            self.presentbuttonwidth = self.buttonfivewidth
        else:
            print 'ERROR!!!!'


    def registerNextButton(self, button):
        button.setGeometry(self.xcursor, self.ycursor, self.presentbuttonwidth, self.presentbuttonheight)
        button.setParentItem(self)
        self.xcursor += self.presentbuttonwidth + self.distance

    
    def skipNextButton(self):
        self.xcursor += self.presentbuttonwidth + self.distance

    
    def fixWindow(self):
        self.setRect(self.windowleftxcoordinate + self.windowframethickness, 
                     self.windowframethickness, self.windowusablewidth, self.ycursor+self.distance)
        
        
    def putWindowAtBottom(self):
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        h = self.boundingRect().height()
        self.moveBy(0, self.windowheight-h-self.windowframethickness)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, enabled = False)
        


class StatusWindowArea(WindowArea):

    def __init__(self):
        super(StatusWindowArea, self).__init__()
        self.dynamictextitems = {}

    def newTextRowLeft(self, text, dynamic=False, identifier=''):

        self.presentbuttonheight = self.textrowheight
        textitem = QtGui.QGraphicsSimpleTextItem(text, parent=self)
        
        if dynamic and identifier:
            self.dynamictextitems[identifier] = textitem
        
        font = QtGui.QFont("Helvetica", 10)
        textitem.setFont(font)
        textitem.setBrush(QtCore.Qt.yellow)
        wtext = int(textitem.boundingRect().width())
        htext = int(textitem.boundingRect().height())
        textitem.setPos(self.xcursor + self.windowframethickness, self.ycursor + self.distance)


    def updateDynamicTextItem(self, identifier, text):
        self.dynamictextitems[identifier].setText(text)


class InputWindowArea(StatusWindowArea):
    
    def __init__(self):
        super(InputWindowArea, self).__init__()

    def newFramedTextRow(self, editable=False): # Accept and Clear buttons as arguments perhaps!?!
        self.presentbuttonheight = self.textrowheight +  self.distance
        
        rectangleitem = QtGui.QGraphicsRectItem()
        
        textitem = MyGraphicsTextItem(editable)  #, parent=self)
        #textitem.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        textitem.setTextWidth(self.windowwidth - self.windowframethickness*3 - self.distance*3) # Why 3? It looks better, but why?
        font = QtGui.QFont("Helvetica", 10)
        textitem.setFont(font)

        wtext = textitem.boundingRect().width()
        htext = textitem.boundingRect().height()
        
        rectangleitem = QtGui.QGraphicsRectItem(self.xcursor + self.windowframethickness, self.ycursor + self.distance, wtext, htext, parent=self)
        rectangleitem.setBrush(QtGui.QBrush(QtCore.Qt.white))
        
        textitem.setParentItem(self)
        
        textitem.setPos(self.xcursor + self.windowframethickness, self.ycursor + self.distance)
        
        
    def registerGraphicsTextItem(self, textitem):
        
        self.presentbuttonheight = self.textrowheight +  self.distance
        #rectangleitem = QtGui.QGraphicsRectItem()
                
        textitem.setTextWidth(self.windowwidth - self.windowframethickness*3 - self.distance*3) # Why 3? It looks better, but why?
        font = QtGui.QFont("Helvetica", 10)
        textitem.setFont(font)

        wtext = textitem.boundingRect().width()
        htext = textitem.boundingRect().height()
        
        rectangleitem = QtGui.QGraphicsRectItem(self.xcursor + self.windowframethickness, self.ycursor + self.distance, wtext, htext, parent=self)
        rectangleitem.setBrush(QtGui.QBrush(QtCore.Qt.white))
        
        textitem.setParentItem(self)
        
        textitem.setPos(self.xcursor + self.windowframethickness, self.ycursor + self.distance)
        
        
        
    
        # So, this is the next challenge!!!

        
#Qt.TextEditable 	The text is fully editable.
#Qt.TextEditorInteraction 	The default for a text editor.



#class MyGraphicsTextItem(QtGui.QGraphicsTextItem):
    
#    def __init__(self, editable=False):
#        super(MyGraphicsTextItem, self).__init__('')
#    
#        if editable:
#            self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
#            
#    def paint(self):
#        pass
            
        