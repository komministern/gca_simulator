#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright © 2016, 2017 Oscar Franzén <oscarfranzen@yahoo.se>
#
#    This file is part of GCA Simulator.


from PySide import QtGui, QtCore


class PlotItem(QtGui.QGraphicsEllipseItem):
    
    def __init__(self, x, y, parent, scene, parent_track):
        self.parent_track = parent_track
        radius = scene.plot_radius
        super(PlotItem, self).__init__(x - radius, y - radius, radius*2, radius*2, parent=parent, scene=scene)

    def remove(self):
        self.scene().removeItem(self)


class CorrelatedPlotItem(PlotItem):
    def __init__(self, x, y, parent, scene, parent_track):
        super(CorrelatedPlotItem, self).__init__(x, y, parent=parent, scene=scene, parent_track=parent_track)
        self.setBrush(self.scene().plot_brush)
        self.setPen(self.scene().plot_pen)
        self.setZValue(self.scene().plot_zvalue)

    def mousePressEvent(self, event):
        self.parent_track.toggleDesignated()


class HistoricPlotItem(PlotItem):
    def __init__(self, x, y, parent, scene, parent_track):
        super(HistoricPlotItem, self).__init__(x, y, parent=parent, scene=scene, parent_track=parent_track)
        self.setBrush(self.scene().historic_plot_brush)
        self.setPen(self.scene().historic_plot_pen)
        self.setZValue(self.scene().historic_plot_zvalue)
        
        
class WhiPlotItem(PlotItem):
    def __init__(self, x, y, parent, scene, parent_track):
        super(WhiPlotItem, self).__init__(x, y, parent=parent, scene=scene, parent_track=parent_track)
        self.setBrush(self.scene().plot_brush)
        self.setPen(self.scene().plot_pen)
        self.setZValue(self.scene().plot_zvalue)
        