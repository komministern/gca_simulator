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

import sys
from PySide2 import QtWidgets
from .view.view import MyView
from .presenter.presenter import MyPresenter    # Order?? presenter-model
from .model.model import MyModel

def main():
    app = QtWidgets.QApplication(sys.argv)
    view = MyView() 
    model = MyModel()
    presenter = MyPresenter(model, view)
    view.show()
    sys.exit(app.exec_())

