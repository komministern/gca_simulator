# -*- coding: utf-8 -*-

#    Copyright � 2016, 2017, 2018 Oscar Franz�n <oscarfranzen@protonmail.com>
#
#    This file is part of GCA Analysis Tool.



from PySide import QtGui, QtCore
from ui_ipdialog import Ui_Dialog
import os
#from presenter.filtercontainer import Filter

class MyIPDialog(QtGui.QDialog, Ui_Dialog):

#    quit = QtCore.Signal()

    def __init__(self, parent=None):
        super(MyIPDialog, self).__init__(parent)

        self.setupUi(self)

        # Ladda fil med senast använda ip nummer

        # Om den inte finns, skapa den med 127.0.0.1 som enda post

        # Ladda comboboxen med posterna i ordning

        # Ladda de fyra spinboxarna med numrena från den första posten i comboboxen


        user_path = os.path.expanduser('~')
        file_name = 'ipaddresses.txt'
        file_path = os.path.join(user_path, file_name)

        try:
            print 'trying reading'
            my_file = open(file_path, 'r')
        except Exception, e:
            print e
            print 'writing'
            my_file = open(file_path, 'w')
            my_file.write('127.0.0.1\n')
            my_file.write('127.0.0.2\n')
            my_file.close()
            my_file = open(file_path, 'r')

        print 'reading'

        #with open(filename,'rb') as f:

        l = []

        while True:
            line = my_file.readline()
            if not line: break
            l.append(line)
        
        print l



        self.buttonBox.accepted.connect(self.acc)
        self.buttonBox.rejected.connect(self.rej)
        #self.buttonBox.clicked.connect(self.cli)

    def acc(self):
        print 'accepted'
        # Kolla om adressen är giltig (?)

        # Om så, för in den först i ip-nummer-filen
        # Returnera ip-numret som sträng


    def rej(self):
        print 'rejected'
        #self.accepted()

    #def cli(self):
    #    print 'clicked'


    