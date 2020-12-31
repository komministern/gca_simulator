

from PySide2 import QtCore, QtWidgets, QtGui

from .plot import HistoricPlotItem

# import random
# import numpy as np

class HistoricUncorrelatedPlots(QtCore.QObject):
    
    def __init__(self, scene):
        super(HistoricUncorrelatedPlots, self).__init__()

        self.scene = scene

        # self.scene.addItem(self)

        # self.setZValue(self.scene.obstruction_zvalue)
        
        # self.obstruction_item = None

        # self.random = random.Random()

        self.historic_plot_points_ttl_list = [[]]

        self.historic_plot_items = []

        #self.calculate()
        #self.create()

    def resetHistoryPlots(self):
        self.historic_plot_points_ttl_list = [[]]

    def update(self, new_historic_plot_points):

        self.historic_plot_points_ttl_list.insert(0, new_historic_plot_points)
        if len(self.historic_plot_points_ttl_list) > 15:
            del self.historic_plot_points_ttl_list[-1]

        


    def draw(self):
        

        for item in self.historic_plot_items:
            item.remove()
        self.historic_plot_items = []
    
        if self.scene.radiating:

            if self.scene.nhist != None:
                i = 0
                for points in self.historic_plot_points_ttl_list:
                    if i < self.scene.nhist:
                        for point in points:
                            self.historic_plot_items.append(HistoricPlotItem(point.x(), point.y(), None, self.scene, None))
                        i += 1
