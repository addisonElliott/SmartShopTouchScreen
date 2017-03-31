# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'purchaseHistoryWindow.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PurchaseHistoryWindow(object):
    def setupUi(self, PurchaseHistoryWindow):
        PurchaseHistoryWindow.setObjectName("PurchaseHistoryWindow")
        PurchaseHistoryWindow.setWindowModality(QtCore.Qt.NonModal)
        PurchaseHistoryWindow.resize(800, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PurchaseHistoryWindow.sizePolicy().hasHeightForWidth())
        PurchaseHistoryWindow.setSizePolicy(sizePolicy)
        PurchaseHistoryWindow.setMaximumSize(QtCore.QSize(855, 661))
        font = QtGui.QFont()
        font.setPointSize(15)
        PurchaseHistoryWindow.setFont(font)
        PurchaseHistoryWindow.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        PurchaseHistoryWindow.setProperty("dockNestingEnabled", False)
        PurchaseHistoryWindow.setProperty("unifiedTitleAndToolBarOnMac", False)
        self.gridLayout = QtWidgets.QGridLayout(PurchaseHistoryWindow)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setContentsMargins(0, -1, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(5, -1, 5, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.backBtn = TouchButton(PurchaseHistoryWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backBtn.sizePolicy().hasHeightForWidth())
        self.backBtn.setSizePolicy(sizePolicy)
        self.backBtn.setMinimumSize(QtCore.QSize(64, 64))
        self.backBtn.setMaximumSize(QtCore.QSize(64, 64))
        self.backBtn.setStyleSheet("background-color: transparent;\n"
"border: 0;")
        self.backBtn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/Icons/BlueBackIcon_Finished.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backBtn.setIcon(icon)
        self.backBtn.setIconSize(QtCore.QSize(64, 64))
        self.backBtn.setObjectName("backBtn")
        self.horizontalLayout_2.addWidget(self.backBtn)
        spacerItem = QtWidgets.QSpacerItem(214, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout_5.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.homeBtn = TouchButton(PurchaseHistoryWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.homeBtn.sizePolicy().hasHeightForWidth())
        self.homeBtn.setSizePolicy(sizePolicy)
        self.homeBtn.setStyleSheet("background-color: transparent;\n"
"border: 0;")
        self.homeBtn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Icons/Icons/SSLogo_No_Background.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.homeBtn.setIcon(icon1)
        self.homeBtn.setIconSize(QtCore.QSize(256, 64))
        self.homeBtn.setCheckable(False)
        self.homeBtn.setChecked(False)
        self.homeBtn.setObjectName("homeBtn")
        self.gridLayout_5.addWidget(self.homeBtn, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(260, 63, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem1, 0, 2, 1, 1)
        self.gridLayout_5.setColumnStretch(0, 1)
        self.gridLayout_5.setColumnStretch(1, 1)
        self.gridLayout_5.setColumnStretch(2, 1)
        self.gridLayout.addLayout(self.gridLayout_5, 2, 0, 1, 2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gridLayout.addLayout(self.horizontalLayout_3, 4, 1, 1, 1)
        self.historyView = QtWidgets.QTableView(PurchaseHistoryWindow)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(21)
        self.historyView.setFont(font)
        self.historyView.setStyleSheet("QTableView::item {\n"
"    border: 0px;\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"}")
        self.historyView.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.historyView.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.historyView.setLineWidth(3)
        self.historyView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.historyView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.historyView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.historyView.setProperty("showDropIndicator", False)
        self.historyView.setAlternatingRowColors(True)
        self.historyView.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.historyView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.historyView.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.historyView.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.historyView.setSortingEnabled(True)
        self.historyView.setWordWrap(False)
        self.historyView.setObjectName("historyView")
        self.historyView.verticalHeader().setVisible(False)
        self.historyView.verticalHeader().setDefaultSectionSize(45)
        self.gridLayout.addWidget(self.historyView, 3, 0, 1, 2)
        self.gridLayout.setColumnStretch(0, 1)

        self.retranslateUi(PurchaseHistoryWindow)
        QtCore.QMetaObject.connectSlotsByName(PurchaseHistoryWindow)

    def retranslateUi(self, PurchaseHistoryWindow):
        _translate = QtCore.QCoreApplication.translate
        PurchaseHistoryWindow.setWindowTitle(_translate("PurchaseHistoryWindow", "Smart Shop"))

from Widgets.touchButton import TouchButton
import Resource_BY_rc
import style_rc
