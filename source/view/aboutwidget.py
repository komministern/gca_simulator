
import os
from PySide2 import QtCore, QtWidgets, QtGui

from mycommonfunctions import path as mypath

from .ui_about import Ui_About

class AboutWidget(QtWidgets.QWidget, Ui_About):

    my_close = QtCore.Signal()

    def __init__(self):
        super(AboutWidget, self).__init__()

        resources_directory = os.path.join(mypath.current_working_directory(), 'resources')
        images_directory = os.path.join(resources_directory, 'images')
        icon_path = os.path.join(images_directory, 'icon.ico')

        self.setWindowIcon(QtGui.QIcon(icon_path))

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