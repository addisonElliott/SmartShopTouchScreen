# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CheckOutBox.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CheckOutBox(object):
    def setupUi(self, CheckOutBox):
        CheckOutBox.setObjectName("CheckOutBox")
        CheckOutBox.resize(380, 243)
        font = QtGui.QFont()
        font.setPointSize(19)
        CheckOutBox.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(CheckOutBox)
        self.gridLayout.setObjectName("gridLayout")
        self.item_label = QtWidgets.QLabel(CheckOutBox)
        font = QtGui.QFont()
        font.setFamily("Cronus Round")
        font.setPointSize(19)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.item_label.setFont(font)
        self.item_label.setObjectName("item_label")
        self.gridLayout.addWidget(self.item_label, 10, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 18, 1, 1, 1)
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        self.cancel_label = QtWidgets.QLabel(CheckOutBox)
        font = QtGui.QFont()
        font.setFamily("Cronus Round")
        font.setPointSize(19)
        self.cancel_label.setFont(font)
        self.cancel_label.setObjectName("cancel_label")
        self.horizontalLayout_1.addWidget(self.cancel_label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_1.addItem(spacerItem1)
        self.accept_button = TouchButton(CheckOutBox)
        self.accept_button.setMinimumSize(QtCore.QSize(45, 45))
        self.accept_button.setMaximumSize(QtCore.QSize(45, 45))
        self.accept_button.setStyleSheet("background-color: #31363B;\n"
"border: 0;")
        self.accept_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/Icons/GreenCheckIcon_Finished.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.accept_button.setIcon(icon)
        self.accept_button.setIconSize(QtCore.QSize(40, 40))
        self.accept_button.setObjectName("accept_button")
        self.horizontalLayout_1.addWidget(self.accept_button)
        self.cancel_button = TouchButton(CheckOutBox)
        self.cancel_button.setMinimumSize(QtCore.QSize(45, 45))
        self.cancel_button.setMaximumSize(QtCore.QSize(45, 45))
        self.cancel_button.setStyleSheet("background-color: #31363B;\n"
"border: 0;")
        self.cancel_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Icons/Icons/RedCancelIcon_Finished.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cancel_button.setIcon(icon1)
        self.cancel_button.setIconSize(QtCore.QSize(40, 40))
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout_1.addWidget(self.cancel_button)
        self.gridLayout.addLayout(self.horizontalLayout_1, 19, 1, 1, 4)
        self.qty_label = QtWidgets.QLabel(CheckOutBox)
        font = QtGui.QFont()
        font.setFamily("Cronus Round")
        font.setPointSize(19)
        self.qty_label.setFont(font)
        self.qty_label.setObjectName("qty_label")
        self.gridLayout.addWidget(self.qty_label, 11, 1, 1, 1)
        self.title_label = QtWidgets.QLabel(CheckOutBox)
        font = QtGui.QFont()
        font.setFamily("Cronus Round")
        font.setPointSize(21)
        self.title_label.setFont(font)
        self.title_label.setObjectName("title_label")
        self.gridLayout.addWidget(self.title_label, 9, 1, 1, 2, QtCore.Qt.AlignHCenter)
        self.item_textBox = QtWidgets.QLineEdit(CheckOutBox)
        self.item_textBox.setObjectName("item_textBox")
        self.gridLayout.addWidget(self.item_textBox, 10, 2, 1, 1)
        self.qty_combo = QtWidgets.QComboBox(CheckOutBox)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.qty_combo.setFont(font)
        self.qty_combo.setObjectName("qty_combo")
        self.gridLayout.addWidget(self.qty_combo, 11, 2, 1, 1, QtCore.Qt.AlignLeft)

        self.retranslateUi(CheckOutBox)
        QtCore.QMetaObject.connectSlotsByName(CheckOutBox)

    def retranslateUi(self, CheckOutBox):
        _translate = QtCore.QCoreApplication.translate
        CheckOutBox.setWindowTitle(_translate("CheckOutBox", "Dialog"))
        self.item_label.setText(_translate("CheckOutBox", "Item"))
        self.cancel_label.setText(_translate("CheckOutBox", "Scan to continue"))
        self.qty_label.setText(_translate("CheckOutBox", "Quantity"))
        self.title_label.setText(_translate("CheckOutBox", "Check Out"))

from Widgets.touchButton import TouchButton
import Resource_BY_rc
import style_rc
