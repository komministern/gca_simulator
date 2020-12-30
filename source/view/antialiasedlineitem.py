
from PySide2 import QtCore, QtWidgets, QtGui


class AntiAliasedLineItem(QtWidgets.QGraphicsLineItem):

    def __init__(self, line_item, parent=None):
        super(AntiAliasedLineItem, self).__init__(line_item, parent=parent)

    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        super(AntiAliasedLineItem, self).paint(painter, option, widget)