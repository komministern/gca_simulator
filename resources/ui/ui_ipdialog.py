# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ipdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(271, 102)
        Dialog.setMinimumSize(QSize(271, 102))
        Dialog.setMaximumSize(QSize(271, 114))
        Dialog.setModal(True)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(64, 16777215))

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.spinBox_1 = QSpinBox(Dialog)
        self.spinBox_1.setObjectName(u"spinBox_1")
        self.spinBox_1.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_1.setMaximum(255)

        self.horizontalLayout.addWidget(self.spinBox_1)

        self.spinBox_2 = QSpinBox(Dialog)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_2.setMaximum(255)

        self.horizontalLayout.addWidget(self.spinBox_2)

        self.spinBox_3 = QSpinBox(Dialog)
        self.spinBox_3.setObjectName(u"spinBox_3")
        self.spinBox_3.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_3.setMaximum(255)

        self.horizontalLayout.addWidget(self.spinBox_3)

        self.spinBox_4 = QSpinBox(Dialog)
        self.spinBox_4.setObjectName(u"spinBox_4")
        self.spinBox_4.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_4.setMinimum(0)
        self.spinBox_4.setMaximum(255)

        self.horizontalLayout.addWidget(self.spinBox_4)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.formLayout.setLayout(0, QFormLayout.SpanningRole, self.horizontalLayout_2)

        self.horizontalSpacer = QSpacerItem(58, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.formLayout.setItem(1, QFormLayout.LabelRole, self.horizontalSpacer)

        self.comboBox = QComboBox(Dialog)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setEditable(False)
        self.comboBox.setInsertPolicy(QComboBox.NoInsert)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboBox)


        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Flight Sim IP Address", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Connect to", None))
    # retranslateUi

