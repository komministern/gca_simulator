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

from .plot import UnCorrelatedPlotItem, HistoricPlotItem

class UncorrelatedPlots(QtCore.QObject):
    
    def __init__(self, scene):
        super(UncorrelatedPlots, self).__init__()

        self.scene = scene

        #self.scene.addItem(self)

        #self.setZValue(self.scene.plot_zvalue)

        self.passive_tracks = []
        
        self.uncorrelated_plot_items = []

        #self.uncorrelated_historic_plot_items = []

    def update(self, passive_tracks):
        self.passive_tracks = passive_tracks

    def draw(self):
        #self.scene.removeItem(self)

        # for ttl_item_list in self.uncorrelated_historic_plot_items:
        #     for item in ttl_item_list:
        #         self.removeFromGroup(item)

        new_historic_plot_points = []
        for item in self.uncorrelated_plot_items:
            item.remove()
            new_historic_plot_points.append(item.getItemPoint())
            
        # Move item to historic plots
        self.scene.historic_uncorrelated_plots_item.update(new_historic_plot_points)
        
        
        
        self.uncorrelated_plot_items = []

        if self.scene.radiating:

            for track in self.passive_tracks:
                el_coord = self.passive_tracks[track].historic_coordinate(0, 'el')
                az_coord = self.passive_tracks[track].historic_coordinate(0, 'az')
                #if not isinstance(el_coord, type(None)):
                if self.passive_tracks[track].targets[0].el_hit:
                    el_point = self.scene.getElevationPoint(el_coord)
                    el_item = UnCorrelatedPlotItem(el_point.x(), el_point.y(), None, self.scene)
                    self.uncorrelated_plot_items.append(el_item)
                    #self.addToGroup(el_item)
                #if not isinstance(az_coord, type(None)):
                if self.passive_tracks[track].targets[0].az_hit:
                    az_point = self.scene.getAzimuthPoint(az_coord)
                    az_item = UnCorrelatedPlotItem(az_point.x(), az_point.y(), None, self.scene)
                    self.uncorrelated_plot_items.append(az_item)
                    #self.addToGroup(az_item)

            #self.scene.addItem(self)

