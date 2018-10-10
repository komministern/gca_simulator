# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ipdialog.ui'
#
# Created: Mon Oct 08 21:34:36 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(271, 102)
        Dialog.setMinimumSize(QtCore.QSize(271, 102))
        Dialog.setMaximumSize(QtCore.QSize(271, 114))
        Dialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtGui.QLabel(Dialog)
        self.label.setMaximumSize(QtCore.QSize(64, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.spinBox_1 = QtGui.QSpinBox(Dialog)
        self.spinBox_1.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.spinBox_1.setMaximum(255)
        self.spinBox_1.setObjectName("spinBox_1")
        self.horizontalLayout.addWidget(self.spinBox_1)
        self.spinBox_2 = QtGui.QSpinBox(Dialog)
        self.spinBox_2.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.spinBox_2.setMaximum(255)
        self.spinBox_2.setObjectName("spinBox_2")
        self.horizontalLayout.addWidget(self.spinBox_2)
        self.spinBox_3 = QtGui.QSpinBox(Dialog)
        self.spinBox_3.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.spinBox_3.setMaximum(255)
        self.spinBox_3.setObjectName("spinBox_3")
        self.horizontalLayout.addWidget(self.spinBox_3)
        self.spinBox_4 = QtGui.QSpinBox(Dialog)
        self.spinBox_4.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.spinBox_4.setMinimum(0)
        self.spinBox_4.setMaximum(255)
        self.spinBox_4.setObjectName("spinBox_4")
        self.horizontalLayout.addWidget(self.spinBox_4)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.formLayout.setLayout(0, QtGui.QFormLayout.SpanningRole, self.horizontalLayout_2)
        spacerItem = QtGui.QSpacerItem(58, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.formLayout.setItem(1, QtGui.QFormLayout.LabelRole, spacerItem)
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setEditable(False)
        self.comboBox.setInsertPolicy(QtGui.QComboBox.NoInsert)
        self.comboBox.setObjectName("comboBox")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBox)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Connect to", None, QtGui.QApplication.UnicodeUTF8))

