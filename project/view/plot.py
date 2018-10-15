#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright © 2016, 2017 Oscar Franzén <oscarfranzen@yahoo.se>
#
#    This file is part of GCA Simulator.


from PySide import QtGui, QtCore


class PlotItem(QtGui.QGraphicsEllipseItem):
    
    def __init__(self, x, y, parent, scene, parent_track, visible):
        self.parent_track = parent_track
        radius = scene.plot_radius
        super(PlotItem, self).__init__(x - radius, y - radius, radius*2, radius*2, parent=parent, scene=scene)
        if visible:
            self.setOpacity(1.0)
        else:
            self.setOpacity(0.0)

    def remove(self):
        self.scene().removeItem(self)


class CorrelatedPlotItem(PlotItem):
    def __init__(self, x, y, parent, scene, parent_track, visible=True):
        super(CorrelatedPlotItem, self).__init__(x, y, parent=parent, scene=scene, parent_track=parent_track, visible=visible)
        self.setBrush(self.scene().plot_brush)
        self.setPen(self.scene().plot_pen)
        self.setZValue(self.scene().plot_zvalue)

    def mousePressEvent(self, event):
        self.parent_track.toggleDesignated()


class UnCorrelatedPlotItem(PlotItem):
    def __init__(self, x, y, parent, scene, parent_track, visible=True):
        super(UnCorrelatedPlotItem, self).__init__(x, y, parent=parent, scene=scene, parent_track=parent_track, visible=visible)
        self.setBrush(QtCore.Qt.red)
        self.setBrush(self.scene().uncorrelated_plot_brush)
        self.setPen(self.scene().uncorrelated_plot_pen)     
        self.setZValue(self.scene().plot_zvalue)

    def mousePressEvent(self, event):
        self.parent_track.toggleDesignated()


class InvisiblePlotItem(PlotItem):
    def __init__(self, x, y, parent, scene, parent_track, visible=False):
        super(InvisiblePlotItem, self).__init__(x, y, parent=parent, scene=scene, parent_track=parent_track, visible=visible)
        self.setBrush(self.scene().plot_brush)
        self.setPen(self.scene().plot_pen)
        self.setZValue(self.scene().plot_zvalue)


class HistoricPlotItem(PlotItem):
    def __init__(self, x, y, parent, scene, parent_track, visible=True):
        super(HistoricPlotItem, self).__init__(x, y, parent=parent, scene=scene, parent_track=parent_track, visible=visible)
        self.setBrush(self.scene().historic_plot_brush)
        self.setPen(self.scene().historic_plot_pen)
        self.setZValue(self.scene().historic_plot_zvalue)
        
        
class WhiPlotItem(PlotItem):
    def __init__(self, x, y, parent, scene, parent_track, visible=True):
        super(WhiPlotItem, self).__init__(x, y, parent=parent, scene=scene, parent_track=parent_track, visible=visible)
        self.setBrush(self.scene().plot_brush)
        self.setPen(self.scene().plot_pen)
        self.setZValue(self.scene().plot_zvalue)
        