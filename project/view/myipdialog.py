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

        self.comboBox.currentIndexChanged.connect(self.indexChanged)

        user_path = os.path.expanduser('~')
        file_name = 'ipaddresses.txt'
        self.file_path = os.path.join(user_path, file_name)

        if not os.path.exists(self.file_path):
            f = open(self.file_path, 'w')
            f.write('127.0.0.1\n')
            f.write('127.0.0.2\n')
            f.close()
        
        self.list_of_ip_adresses = [] 
        with open(self.file_path,'r') as f:
            self.list_of_ip_adresses = [line.rstrip('\n') for line in f]
            
            #if not adress:  break
            #list_of_ip_adresses.append(adress.replace('\n', ''))

        self.comboBox.clear()
        self.comboBox.addItems(self.list_of_ip_adresses)

        self.comboBox.setCurrentIndex(0)
        
        #print self.list_of_ip_adresses



#lines = [line.rstrip('\n') for line in file]




        self.buttonBox.accepted.connect(self.acc)
        self.buttonBox.rejected.connect(self.rej)
        #self.buttonBox.clicked.connect(self.cli)

    def indexChanged(self):

        spin_boxes = [self.spinBox_1, self.spinBox_2, self.spinBox_3, self.spinBox_4]
        values = self.comboBox.currentText().split('.')
        print '--------------------------'
        print values
        for spin_box, value in zip(spin_boxes, values):
            spin_box.setValue(int(value))
        
        #print groups

    def acc(self):
        #print 'accepted'
        # Kolla om adressen är giltig (?) - No
        
        spin_boxes = [self.spinBox_1, self.spinBox_2, self.spinBox_3, self.spinBox_4]
        values = [str(spin_box.value()) for spin_box in spin_boxes]

        adress = '.'.join(values)

        if not adress in self.list_of_ip_adresses:
            print 'new adress'
            self.list_of_ip_adresses.insert(0, adress)
        
            self.comboBox.clear()
            self.comboBox.addItems(self.list_of_ip_adresses)
            self.comboBox.setCurrentIndex(0)


        
        self.accept()



        # Om så, för in den först i ip-nummer-filen
        # Returnera ip-numret som sträng


    def rej(self):
        print 'rejected'
        self.reject()

    #def cli(self):
    #    print 'clicked'


    