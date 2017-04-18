#!/usr/bin/env python

import os

os.system('pyside-uic mainwindow.ui -o mainwindow.py')
os.system('cp mainwindow.py ../project/view/.')

