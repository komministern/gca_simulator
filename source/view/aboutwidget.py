
import os
from PySide2 import QtCore, QtWidgets, QtGui

from mycommonfunctions import path as mypath
from mycommonfunctions import basicconfig as myconf

from .ui_about import Ui_About

globalvars = myconf.getGlobals()

class AboutWidget(QtWidgets.QWidget, Ui_About):

    my_close = QtCore.Signal()

    def __init__(self):
        super(AboutWidget, self).__init__()

        # resources_directory = os.path.join(mypath.current_working_directory(), 'resources')
        # images_directory = os.path.join(resources_directory, 'images')
        # icon_path = os.path.join(images_directory, 'icon.ico')

        # self.setWindowIcon(QtGui.QIcon(icon_path))

        self.setWindowIcon(QtGui.QIcon(globalvars['icon_file']))

        self.setupUi(self)

        self.label_version.setText(globalvars['version'])

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