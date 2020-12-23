
from PySide2 import QtCore, QtWidgets

from .ui_about import Ui_About

class AboutWidget(QtWidgets.QWidget, Ui_About):

    my_close = QtCore.Signal()

    def __init__(self):
        super(AboutWidget, self).__init__()
        self.setupUi(self)
        self.closedfrombutton = False

    def closeEvent(self, event):
        #print('closeEvent()')
        #print(self.closedfrombutton)
        if not self.closedfrombutton:
            self.my_close.emit()
            #print('my_close.emit()')
        self.closedfrombutton = False
        super(AboutWidget, self).closeEvent(event)

    def close(self):
        #print('close()')
        self.closedfrombutton = True
        super(AboutWidget, self).close()