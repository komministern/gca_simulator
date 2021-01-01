﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright © 2016, 2017 Oscar Franzén <oscarfranzen@yahoo.se>
#
#    This file is part of GCA Simulator.


from PySide2 import QtCore, QtWidgets, QtGui

class PlotItem(QtWidgets.QGraphicsEllipseItem):
    
    def __init__(self, x, y, parent, scene, parent_track, visible):
        self.parent_track = parent_track
        self.scene = scene

        radius = scene.plot_radius
        super(PlotItem, self).__init__(x - radius, y - radius, radius*2, radius*2, parent=parent)

        self.scene.addItem(self)

        if visible:
            self.setOpacity(1.0)
        else:
            self.setOpacity(0.0)

    def remove(self):
        self.scene.removeItem(self)

    def getItemPoint(self):
        return QtCore.QPointF(self.rect().x() + self.scene.plot_radius, self.rect().y() + self.scene.plot_radius)


class CorrelatedTrackedPlotItem(PlotItem):
    def __init__(self, x, y, parent, scene, parent_track, visible=True):
        super(CorrelatedTrackedPlotItem, self).__init__(x, y, parent=parent, scene=scene, parent_track=parent_track, visible=visible)
        self.setBrush(self.scene.plot_brush)
        self.setPen(self.scene.plot_pen)
        self.setZValue(self.scene.plot_zvalue)

    def mousePressEvent(self, event):
        self.parent_track.toggleDesignated()
    
class UnCorrelatedTrackedPlotItem(PlotItem):
    def __init__(self, x, y, parent, scene, parent_track, visible=True):
        super(UnCorrelatedTrackedPlotItem, self).__init__(x, y, parent=parent, scene=scene, parent_track=parent_track, visible=visible)
        # self.setBrush(self.scene.plot_brush)
        # self.setPen(self.scene.plot_pen)

        self.setBrush(self.scene.uncorrelated_plot_brush)
        self.setPen(self.scene.uncorrelated_plot_pen)   

        self.setZValue(self.scene.plot_zvalue)

    def mousePressEvent(self, event):
        self.parent_track.toggleDesignated()


class CorrelatedPlotItem(PlotItem):
    def __init__(self, x, y, parent, scene, visible=True):
        super(CorrelatedPlotItem, self).__init__(x, y, parent=parent, scene=scene, visible=visible)
        self.setBrush(self.scene.plot_brush)
        self.setPen(self.scene.plot_pen)
        self.setZValue(self.scene.plot_zvalue)

    # def mousePressEvent(self, event):
    #     self.parent_track.toggleDesignated()


class UnCorrelatedPlotItem(PlotItem):
    def __init__(self, x, y, parent, scene, visible=True):
        super(UnCorrelatedPlotItem, self).__init__(x, y, parent=parent, scene=scene, parent_track=None, visible=visible)
        self.setBrush(QtCore.Qt.red)
        self.setBrush(self.scene.uncorrelated_plot_brush)
        self.setPen(self.scene.uncorrelated_plot_pen)     
        self.setZValue(self.scene.plot_zvalue)

    # def mousePressEvent(self, event):
    #     self.parent_track.toggleDesignated()


class InvisiblePlotItem(PlotItem):
    def __init__(self, x, y, parent, scene, parent_track, visible=False):
        super(InvisiblePlotItem, self).__init__(x, y, parent=parent, scene=scene, parent_track=parent_track, visible=visible)
        self.setBrush(self.scene.plot_brush)
        self.setPen(self.scene.plot_pen)
        self.setZValue(self.scene.plot_zvalue)


class HistoricPlotItem(PlotItem):
    def __init__(self, x, y, parent, scene, parent_track, visible=True):
        super(HistoricPlotItem, self).__init__(x, y, parent=parent, scene=scene, parent_track=parent_track, visible=visible)
        self.setBrush(self.scene.historic_plot_brush)
        self.setPen(self.scene.historic_plot_pen)
        self.setZValue(self.scene.historic_plot_zvalue)
        
        
class WhiPlotItem(PlotItem):
    def __init__(self, x, y, parent, scene, parent_track, visible=True):
        super(WhiPlotItem, self).__init__(x, y, parent=parent, scene=scene, parent_track=parent_track, visible=visible)
        self.setBrush(self.scene.plot_brush)
        self.setPen(self.scene.plot_pen)
        self.setZValue(self.scene.plot_zvalue)



        