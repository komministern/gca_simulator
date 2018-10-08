#!python

import os
import shutil

os.system('pyside-uic ipdialog.ui -o ui_ipdialog.py')
shutil.copyfile('./ui_ipdialog.py', '../project/view/ui_ipdialog.py')
