

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
        
        self.uncorrelated_plot_items = []

        self.scene.historic_uncorrelated_plots_item.update(new_historic_plot_points)

        #self.uncorrelated_historic_plot_items.insert(0, new_historic_plot_items)

        # if len(self.uncorrelated_historic_plot_items) > 15:
        #     del self.uncorrelated_historic_plot_items[-1]

        # for ttl_item_list in self.uncorrelated_historic_plot_items:
        #     for item in ttl_item_list:
        #         self.addToGroup(item)

        if self.scene.radiating:

            for track in self.passive_tracks:
                el_coord = self.passive_tracks[track].historic_coordinate(0, 'el')
                az_coord = self.passive_tracks[track].historic_coordinate(0, 'az')
                if not isinstance(el_coord, type(None)):
                    el_point = self.scene.getElevationPoint(el_coord)
                    el_item = UnCorrelatedPlotItem(el_point.x(), el_point.y(), None, self.scene)
                    self.uncorrelated_plot_items.append(el_item)
                    #self.addToGroup(el_item)
                if not isinstance(az_coord, type(None)):
                    az_point = self.scene.getAzimuthPoint(az_coord)
                    az_item = UnCorrelatedPlotItem(az_point.x(), az_point.y(), None, self.scene)
                    self.uncorrelated_plot_items.append(az_item)
                    #self.addToGroup(az_item)

            #self.scene.addItem(self)

