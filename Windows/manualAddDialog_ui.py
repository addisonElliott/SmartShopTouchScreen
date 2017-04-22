# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'manualAddDialog.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ManualAddDialog(object):
    def setupUi(self, ManualAddDialog):
        ManualAddDialog.setObjectName("ManualAddDialog")
        ManualAddDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ManualAddDialog.resize(487, 286)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ManualAddDialog.sizePolicy().hasHeightForWidth())
        ManualAddDialog.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Cronus Round")
        ManualAddDialog.setFont(font)
        ManualAddDialog.setStyleSheet("QDialog\n"
"{\n"
"    border: 1px solid #76797C;\n"
"}")
        ManualAddDialog.setSizeGripEnabled(False)
        ManualAddDialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(ManualAddDialog)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setObjectName("gridLayout")
        self.nameEdit = TouchLineEdit(ManualAddDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.nameEdit.setFont(font)
        self.nameEdit.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.nameEdit.setMaxLength(20)
        self.nameEdit.setClearButtonEnabled(False)
        self.nameEdit.setObjectName("nameEdit")
        self.gridLayout.addWidget(self.nameEdit, 4, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(ManualAddDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(ManualAddDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setSpacing(15)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.warningLabel = QtWidgets.QLabel(ManualAddDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.warningLabel.setFont(font)
        self.warningLabel.setStyleSheet("QLabel\n"
"{\n"
"    color: red;\n"
"}")
        self.warningLabel.setObjectName("warningLabel")
        self.horizontalLayout_2.addWidget(self.warningLabel, 0, QtCore.Qt.AlignHCenter)
        self.confirmBtn = TouchButton(ManualAddDialog)
        self.confirmBtn.setMinimumSize(QtCore.QSize(48, 48))
        self.confirmBtn.setMaximumSize(QtCore.QSize(48, 48))
        self.confirmBtn.setStyleSheet("background-color: transparent;\n"
"border: 0;")
        self.confirmBtn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/Icons/GreenCheckIcon_Finished.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.confirmBtn.setIcon(icon)
        self.confirmBtn.setIconSize(QtCore.QSize(48, 48))
        self.confirmBtn.setDefault(True)
        self.confirmBtn.setObjectName("confirmBtn")
        self.horizontalLayout_2.addWidget(self.confirmBtn)
        self.cancelBtn = TouchButton(ManualAddDialog)
        self.cancelBtn.setMinimumSize(QtCore.QSize(48, 48))
        self.cancelBtn.setMaximumSize(QtCore.QSize(48, 48))
        self.cancelBtn.setStyleSheet("background-color: transparent;\n"
"border: 0;")
        self.cancelBtn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Icons/Icons/RedCancelIcon_Finished.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cancelBtn.setIcon(icon1)
        self.cancelBtn.setIconSize(QtCore.QSize(48, 48))
        self.cancelBtn.setObjectName("cancelBtn")
        self.horizontalLayout_2.addWidget(self.cancelBtn)
        self.gridLayout.addLayout(self.horizontalLayout_2, 6, 0, 1, 1)
        self.categoryComboBox = QtWidgets.QComboBox(ManualAddDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.categoryComboBox.setFont(font)
        self.categoryComboBox.setObjectName("categoryComboBox")
        self.gridLayout.addWidget(self.categoryComboBox, 2, 0, 1, 1)
        self.favoritesCheckbox = TouchCheckbox(ManualAddDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.favoritesCheckbox.setFont(font)
        self.favoritesCheckbox.setObjectName("favoritesCheckbox")
        self.gridLayout.addWidget(self.favoritesCheckbox, 5, 0, 1, 1)

        self.retranslateUi(ManualAddDialog)
        QtCore.QMetaObject.connectSlotsByName(ManualAddDialog)
        ManualAddDialog.setTabOrder(self.categoryComboBox, self.nameEdit)
        ManualAddDialog.setTabOrder(self.nameEdit, self.confirmBtn)
        ManualAddDialog.setTabOrder(self.confirmBtn, self.cancelBtn)

    def retranslateUi(self, ManualAddDialog):
        _translate = QtCore.QCoreApplication.translate
        ManualAddDialog.setWindowTitle(_translate("ManualAddDialog", "Dialog"))
        self.label_3.setText(_translate("ManualAddDialog", "Item Name"))
        self.label_2.setText(_translate("ManualAddDialog", "Product Category"))
        self.warningLabel.setText(_translate("ManualAddDialog", "Item Already Exists!"))
        self.favoritesCheckbox.setText(_translate("ManualAddDialog", "Add Item to Favorites"))

from Widgets.touchButton import TouchButton
from Widgets.touchCheckbox import TouchCheckbox
from Widgets.touchLineEdit import TouchLineEdit
import Resource_BY_rc
import style_rc
