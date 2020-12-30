

from PySide2 import QtCore, QtWidgets, QtGui


class AzimuthScaleTextItem(QtWidgets.QGraphicsSimpleTextItem):

    def __init__(self, text, value=None, parent=None):
        super(AzimuthScaleTextItem, self).__init__(text, parent=parent)
        self.value = value

    def mousePressEvent(self, event):
        self.scene().az_offset_pressed.emit(self)

    
