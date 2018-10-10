# -*- coding: utf-8 -*-

#    Copyright � 2016, 2017, 2018 Oscar Franz�n <oscarfranzen@protonmail.com>
#
#    This file is part of GCA Analysis Tool.



from PySide import QtGui, QtCore
from ui_ipdialog import Ui_Dialog
import os

class MyIPDialog(QtGui.QDialog, Ui_Dialog):


    def __init__(self, parent=None):
        super(MyIPDialog, self).__init__(parent)

        self.setupUi(self)

        self.comboBox.currentIndexChanged.connect(self.indexChanged)

        user_path = os.path.expanduser('~')
        file_name = 'ipaddresses.txt'
        self.file_path = os.path.join(user_path, file_name)

        if not os.path.exists(self.file_path):
            self.save_ip_adresses(self.file_path, ['127.0.0.1'])
        
        self.list_of_ip_adresses = self.read_ip_adresses(self.file_path)

        self.comboBox.clear()
        self.comboBox.addItems(self.list_of_ip_adresses)
        self.comboBox.setCurrentIndex(0)
        
        self.buttonBox.accepted.connect(self.acc)
        self.buttonBox.rejected.connect(self.rej)

    def save_ip_adresses(self, file_path, list_of_adresses):    # Only save the first five adresses
        f = open(file_path, 'w')
        counter = 0
        for each in list_of_adresses:
            f.write(each + '\n')
            counter += 1
            if counter == 5: 
                break
        f.close()

    def read_ip_adresses(self, file_path):
        with open(file_path,'r') as f:
            list_of_ip_adresses = [line.rstrip('\n') for line in f]
        return list_of_ip_adresses


    def indexChanged(self):
        spin_boxes = [self.spinBox_1, self.spinBox_2, self.spinBox_3, self.spinBox_4]
        values = self.comboBox.currentText().split('.')

        if len(values) == 4:
            for spin_box, value in zip(spin_boxes, values):
                spin_box.setValue(int(value))


    def acc(self):
        spin_boxes = [self.spinBox_1, self.spinBox_2, self.spinBox_3, self.spinBox_4]
        values = [str(spin_box.value()) for spin_box in spin_boxes]

        adress = '.'.join(values)

        if not adress in self.list_of_ip_adresses:
            self.list_of_ip_adresses.insert(0, adress)
            self.comboBox.clear()
            self.comboBox.addItems(self.list_of_ip_adresses)
            self.comboBox.setCurrentIndex(0)
            self.save_ip_adresses(self.file_path, self.list_of_ip_adresses)
        
        self.accept()


    def active_ip_adress(self):
        return self.comboBox.currentText()


    def rej(self):
        self.reject()



    