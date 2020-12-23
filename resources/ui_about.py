# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_About(object):
    def setupUi(self, About):
        if not About.objectName():
            About.setObjectName(u"About")
        About.resize(387, 259)
        self.gridLayout = QGridLayout(About)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(About)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(28)
        self.label.setFont(font)
        self.label.setScaledContents(True)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


        self.retranslateUi(About)

        QMetaObject.connectSlotsByName(About)
    # setupUi

    def retranslateUi(self, About):
        About.setWindowTitle(QCoreApplication.translate("About", u"Form", None))
        self.label.setText(QCoreApplication.translate("About", u"JESUS LEVER", None))
    # retranslateUi

