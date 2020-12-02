#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    Copyright � 2016, 2017 Oscar Franz�n <oscarfranzen@yahoo.se>
#
#    This file is part of GCA Simulator.


from PySide2 import QtCore, QtWidgets, QtGui

import time
from .scene import MyScene


class WindowTopBorder(QtCore.QObject, QtWidgets.QGraphicsRectItem):

    windowleftxcoordinate = MyScene.buttonwindowareatopleft_x
    windowwidth = MyScene.buttonwindowareawidth

    windowframethickness = 3
    windowusablewidth = windowwidth - 2*windowframethickness
    
    #borderthickness = 26
    borderthickness = 22
    
    closerectside = 18
    crossthickness = 2
    
    window_gets_shown = QtCore.Signal()
    window_gets_hidden = QtCore.Signal()
    window_gets_focus = QtCore.Signal()
    window_loses_focus = QtCore.Signal()

    
    def __init__(self, text):   #, update_when_made_visible=False):
        
        
        #super(WindowTopBorder, self).__init__()
        QtCore.QObject.__init__(self)
        QtWidgets.QGraphicsRectItem.__init__(self)
        
        #self.shadow_effect = QtGui.QGraphicsDropShadowEffect()
        #self.shadow_effect.setOffset(1.0, 1.0)
        #self.shadow_effect.setColor(QtCore.Qt.black)

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        
        self.setRect(self.windowleftxcoordinate + self.windowframethickness, 
        self.windowframethickness, self.windowusablewidth, self.borderthickness)
        
        self.window_top_border_unfocused_color = QtGui.QColor(239, 235, 231, 255)
        self.window_top_border_focused_color = QtGui.QColor(107, 153, 194, 255)

        self.window_top_border_font = QtGui.QFont("Helvetica", 10)
        self.window_top_border_font.setStretch(QtGui.QFont.Expanded)
        self.window_top_border_font.setBold(True)

        pen = QtGui.QPen()
        pen.setWidth(self.windowframethickness)
        pen.setColor(self.window_top_border_unfocused_color)
        
        brush = QtGui.QBrush(self.window_top_border_unfocused_color)
        self.setBrush(brush)
        self.setPen(pen)

        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)

        self.setAcceptHoverEvents(True)
        
        #self.update_when_made_visible = update_when_made_visible


        # The following section should be solved differently (see the updateTopBorderText method further down)

        #font = QtGui.QFont("Helvetica", 10)
        #ont.setStretch(QtGui.QFont.Expanded)
        #font.setBold(True)
        self.textitem = QtWidgets.QGraphicsSimpleTextItem(text, parent=self)
            
        self.textitem.setFont(self.window_top_border_font)
        self.textitem.setBrush(QtCore.Qt.black)
            
        textwidth = int(self.textitem.boundingRect().width())
        textheight = int(self.textitem.boundingRect().height())
        
        topborderrect = self.rect()
        winx = topborderrect.x()
        winy = topborderrect.y()
        winwidth = topborderrect.width()
        winheight = topborderrect.height()
        
        self.textitem.setPos(winx+(winwidth-textwidth)/2, winy+(winheight-textheight)/2)

        #self.textitem.setGraphicsEffect(self.shadow_effect)

        # ................

        #self.textitem = None
        #self.updateTopBorderText(text)
        
        d = (winheight-self.closerectside)/2
        self.closeRect = QtWidgets.QGraphicsRectItem(winx+winwidth-self.closerectside-d, winy+d, self.closerectside, self.closerectside, parent=self)
        closerectcolor = QtGui.QColor(54, 78, 99, 255)
        self.closeRect.setPen(QtGui.QPen(closerectcolor))

        crosscenter = self.closeRect.rect().center()
        xcenter = crosscenter.x()
        ycenter = crosscenter.y()
        
        c = self.closerectside/4
        
        self.crossline1 = QtWidgets.QGraphicsLineItem(xcenter-c, ycenter-c, xcenter+c, ycenter+c, parent=self)
        self.crossline2 = QtWidgets.QGraphicsLineItem(xcenter-c, ycenter+c, xcenter+c, ycenter-c, parent=self)
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
        
        #font = QtGui.QFont("Helvetica", 10)     # This font should be taken directly from the scene instead!!!
        #font.setBold(True)
        
        self.textitem = QtWidgets.QGraphicsSimpleTextItem(text, parent=self)
            
        self.textitem.setFont(self.window_top_border_font)
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
        self.setBrush(self.window_top_border_focused_color)
        
        pen = QtGui.QPen()
        pen.setWidth(self.windowframethickness)
        pen.setColor(self.window_top_border_focused_color)
        self.setPen(pen)
        
        self.textitem.setBrush(QtCore.Qt.white)
        
        pen = QtGui.QPen()
        pen.setWidth(self.crossthickness)
        pen.setColor(QtCore.Qt.white)
        self.crossline1.setPen(pen)
        self.crossline2.setPen(pen)
        
#        if self.initial_focus_item != None:
#            self.initial_focus_item.setFocus()

        self.shadow_effect = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow_effect.setOffset(1.0, 1.0)
        self.shadow_effect.setColor(QtCore.Qt.black)

        self.textitem.setGraphicsEffect(self.shadow_effect)

        self.window_gets_focus.emit()
        

        
    def setUnFocused(self):
        
        self.setBrush(self.window_top_border_unfocused_color)
        pen = QtGui.QPen()
        pen.setWidth(self.windowframethickness)
        pen.setColor(self.window_top_border_unfocused_color)
        self.setPen(pen)
        
        self.textitem.setBrush(QtCore.Qt.black)

        pen = QtGui.QPen()
        pen.setWidth(self.crossthickness)
        pen.setColor(QtCore.Qt.black)
        self.crossline1.setPen(pen)
        self.crossline2.setPen(pen)

        self.textitem.setGraphicsEffect(None)
        
        self.window_loses_focus.emit()


    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemPositionChange:
            value.setX(0.0)
            if value.y() < 0:
                value.setY(0.0)
            # The value 761.0 is taken directly (quite ugly) from the mainwindowarea after it beeing created and moved
            # to the bottom of the screen. Horrific.
            
            c = 695.0

            #if value.y() > 761.0 - self.boundingRect().height() - self.childrenBoundingRect().height() + self.windowframethickness:
            #    value.setY(761.0 - self.boundingRect().height() - self.childrenBoundingRect().height() + self.windowframethickness)
            if value.y() > c  - self.childrenBoundingRect().height() - 2*self.windowframethickness:
                value.setY(c  - self.childrenBoundingRect().height() - 2*self.windowframethickness)

        return super(WindowTopBorder, self).itemChange(change, value)  # <<<<< Must return the result !!!

    def mousePressEvent(self, event):
        
        if self.closeRect.rect().contains(event.pos()):
            
            if self.activatingbutton:
                self.activatingbutton.toggleExpanded()
                self.activatingbutton = None
            self.hideWindow()
        else:
        
            self.setFocused()
        


class WindowArea(QtCore.QObject, QtWidgets.QGraphicsRectItem):
    
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
    
    buttonhalfheight = buttonfourwidth / 2.2
    buttonfullheight = 2 * buttonhalfheight
    #buttonhalfheight = buttonfivewidth / 2
    #buttonfullheight = buttonfivewidth

    textrowheight = 24

    lineseparatorthickness = 2
    lineseparatorheight = distance


    def __init__(self):
        
        QtCore.QObject.__init__(self)
        QtWidgets.QGraphicsRectItem.__init__(self)
        

        self.setRect(self.windowleftxcoordinate + self.windowframethickness, 
                     self.windowframethickness, self.windowusablewidth, 800)

        pen = QtGui.QPen()
        pen.setWidth(self.windowframethickness)
        pen.setColor(QtGui.QColor(239, 235, 231, 255))
        self.setPen(pen)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127, 255))
        self.setBrush(brush)


        self.text_row_narrow_font = QtGui.QFont("Helvetica", 10)
        self.text_row_wide_font = QtGui.QFont("Helvetica", 10)
        self.text_row_wide_font.setStretch(QtGui.QFont.Expanded)


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
        self.setFlags(QtWidgets.QGraphicsItem.ItemStacksBehindParent)


    def newTextRow(self, text, size='narrow'):
        self.presentbuttonheight = self.textrowheight
        textitem = QtWidgets.QGraphicsSimpleTextItem(text, parent=self)
        #font = QtGui.QFont("Helvetica", 10)
        #textitem.setFont(self.text_row_font)
        
        if size == 'wide':
            textitem.setFont(self.text_row_wide_font)
        elif size == 'narrow':
            textitem.setFont(self.text_row_narrow_font)
        else:
            raise ValueError('Size in Windowarea.newTextRow must be either widw or narrow.')
        
        textitem.setBrush(QtCore.Qt.yellow)
        wtext = int(textitem.boundingRect().width())
        htext = int(textitem.boundingRect().height())
        textitem.setPos(self.xcursor+(self.windowusablewidth-wtext)/2, self.ycursor+self.distance)

    def newWhiteLineSeparator(self):
        self.presentbuttonheight = self.lineseparatorheight
        pen = QtGui.QPen()
        pen.setWidth(self.lineseparatorthickness)
        pen.setColor(QtCore.Qt.white)
        
        line = QtWidgets.QGraphicsLineItem(self.windowleftxcoordinate+2*self.lineseparatorthickness, self.ycursor+self.distance, self.windowleftxcoordinate+self.windowwidth-2*self.lineseparatorthickness, self.ycursor+self.distance)
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
            print('ERROR!!!!')

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
            print('ERROR!!!!')


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
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        h = self.boundingRect().height()
        self.moveBy(0, self.windowheight-h-self.windowframethickness)
        print(self.windowheight-h-self.windowframethickness)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, enabled = False)
        


class StatusWindowArea(WindowArea):

    def __init__(self):
        super(StatusWindowArea, self).__init__()
        self.dynamictextitems = {}

    def newTextRowLeft(self, text, dynamic=False, identifier=''):

        self.presentbuttonheight = self.textrowheight
        textitem = QtWidgets.QGraphicsSimpleTextItem(text, parent=self)
        
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

    #def newFramedTextRow(self, editable=False): # Accept and Clear buttons as arguments perhaps!?!
    #    self.presentbuttonheight = self.textrowheight +  self.distance
    #    
    #    rectangleitem = QtGui.QGraphicsRectItem()
    #    
    #    textitem = MyGraphicsTextItem(editable)  #, parent=self)
    #    #textitem.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
    #    textitem.setTextWidth(self.windowwidth - self.windowframethickness*3 - self.distance*3) # Why 3? It looks better, but why?
    #    font = QtGui.QFont("Helvetica", 10)
    #    textitem.setFont(font)

    #    wtext = textitem.boundingRect().width()
    #    htext = textitem.boundingRect().height()
        
    #    rectangleitem = QtGui.QGraphicsRectItem(self.xcursor + self.windowframethickness, self.ycursor + self.distance, wtext, htext, parent=self)
    #    rectangleitem.setBrush(QtGui.QBrush(QtCore.Qt.white))
        
    #    textitem.setParentItem(self)
        
    #    textitem.setPos(self.xcursor + self.windowframethickness, self.ycursor + self.distance)
        
        
    def registerGraphicsTextItem(self, textitem):
        
        self.presentbuttonheight = self.textrowheight +  self.distance
        #rectangleitem = QtGui.QGraphicsRectItem()
                
        textitem.setTextWidth(self.windowwidth - self.windowframethickness*3 - self.distance*3) # Why 3? It looks better, but why?
        font = QtGui.QFont("Helvetica", 10)
        
        textitem.setFont(font)

        wtext = textitem.boundingRect().width()
        htext = textitem.boundingRect().height()
        
        rectangleitem = QtWidgets.QGraphicsRectItem(self.xcursor + self.windowframethickness, self.ycursor + self.distance, wtext, htext, parent=self)
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



class LegendWindowArea(WindowArea):

    def __init__(self):
        super(LegendWindowArea, self).__init__()

        brush = QtGui.QBrush(QtGui.QColor(20,20,30,255))
        self.setBrush(brush)

        self.d = 10.0
        self.narrow_column_width = self.windowusablewidth/10.0
        self.wide_column_width = self.windowusablewidth/2.0 - 2*self.d - self.narrow_column_width
        
        self.column_x = {}
        self.column_x[0] = self.windowleftxcoordinate + self.windowframethickness + self.d
        self.column_x[1] = self.column_x[0] + self.narrow_column_width + self.d
        self.column_x[2] = self.column_x[1] + self.wide_column_width + self.d
        self.column_x[3] = self.column_x[2] + self.wide_column_width + self.d

        textitem = QtWidgets.QGraphicsSimpleTextItem('42', parent=self)
        font = QtGui.QFont("Helvetica", 10)
        textitem.setFont(font)

        self.thincolorbar_height = textitem.boundingRect().height()
        
        self.thickcolorbar_height = 3*self.textrowheight - self.thincolorbar_height
        
        self.colorbar_width = self.wide_column_width


    def setColumn(self, column):
        self.ycursor = self.d
        self.xcursor = self.column_x[column]


    def newText(self, text):

        textitem = QtWidgets.QGraphicsSimpleTextItem(text, parent=self)
        
        font = QtGui.QFont("Helvetica", 10)
        font.setStretch(QtGui.QFont.Expanded)
        textitem.setFont(font)
        textitem.setBrush(QtCore.Qt.white)
        textitem.setPos(self.xcursor, self.ycursor)

    def newThinColorBar(self, color):
        rect = QtCore.QRectF(self.xcursor, self.ycursor, self.colorbar_width, self.thincolorbar_height)
        rectitem = QtWidgets.QGraphicsRectItem(rect, parent=self)
        brush = QtGui.QBrush(color)
        rectitem.setBrush(brush)

    def newThickColorBar(self, color):
        rect = QtCore.QRectF(self.xcursor, self.ycursor + self.thincolorbar_height/2.0 - self.thickcolorbar_height/2, self.colorbar_width, self.thickcolorbar_height)
        rectitem = QtWidgets.QGraphicsRectItem(rect, parent=self)
        brush = QtGui.QBrush(color)
        rectitem.setBrush(brush)

    def endRow(self, n=1):
        self.ycursor += n*self.textrowheight
