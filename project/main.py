#!/usr/bin/env python
# -*- coding: utf-8 -*-


#    Copyright © 2016, 2017 Oscar Franzén <oscarfranzen@yahoo.se>
#
#    This file is part of GCA Analysis Tool.


import sys
from PySide import QtGui
from view.view import MyView
from presenter.presenter import MyPresenter
from model.model import MyModel


if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)

    view = MyView() 
    model = MyModel()
    presenter = MyPresenter(model, view)
    
    view.show()
#    view.showFullScreen()


    sys.exit(app.exec_())

