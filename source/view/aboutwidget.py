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