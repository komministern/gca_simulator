#!python

import os
import shutil

os.system('pyside2-uic ipdialog.ui -o ui_ipdialog.py')
shutil.copyfile('./ui_ipdialog.py', '../source/view/ui_ipdialog.py')

os.system('pyside2-uic about.ui -o ui_about.py')
shutil.copyfile('./ui_about.py', '../source/view/ui_about.py')
