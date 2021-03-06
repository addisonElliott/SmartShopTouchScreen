# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingsWindow.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.setWindowModality(QtCore.Qt.NonModal)
        SettingsWindow.resize(800, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SettingsWindow.sizePolicy().hasHeightForWidth())
        SettingsWindow.setSizePolicy(sizePolicy)
        SettingsWindow.setMaximumSize(QtCore.QSize(855, 661))
        font = QtGui.QFont()
        font.setPointSize(15)
        SettingsWindow.setFont(font)
        SettingsWindow.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        SettingsWindow.setProperty("dockNestingEnabled", False)
        SettingsWindow.setProperty("unifiedTitleAndToolBarOnMac", False)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(SettingsWindow)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setContentsMargins(0, -1, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(5, -1, 5, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.backBtn = TouchButton(SettingsWindow)
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
        self.homeBtn = TouchButton(SettingsWindow)
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
        self.verticalLayout_3.addLayout(self.gridLayout_5)
        self.settingsStack = QtWidgets.QStackedWidget(SettingsWindow)
        self.settingsStack.setObjectName("settingsStack")
        self.mainPage = QtWidgets.QWidget()
        self.mainPage.setObjectName("mainPage")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.mainPage)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.settingsView = QtWidgets.QListWidget(self.mainPage)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(25)
        self.settingsView.setFont(font)
        self.settingsView.setStyleSheet("QTableView::item {\n"
"    border: 0px;\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"}")
        self.settingsView.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.settingsView.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.settingsView.setLineWidth(3)
        self.settingsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.settingsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.settingsView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.settingsView.setProperty("showDropIndicator", False)
        self.settingsView.setAlternatingRowColors(True)
        self.settingsView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.settingsView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.settingsView.setIconSize(QtCore.QSize(64, 64))
        self.settingsView.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.settingsView.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.settingsView.setMovement(QtWidgets.QListView.Static)
        self.settingsView.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.settingsView.setViewMode(QtWidgets.QListView.ListMode)
        self.settingsView.setModelColumn(0)
        self.settingsView.setUniformItemSizes(False)
        self.settingsView.setSelectionRectVisible(False)
        self.settingsView.setObjectName("settingsView")
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(35)
        item.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Icons/Icons/BlueSettingsIcon_Finished.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon2)
        self.settingsView.addItem(item)
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(35)
        item.setFont(font)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Icons/Icons/Algorithm_Finished.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon3)
        self.settingsView.addItem(item)
        self.gridLayout_2.addWidget(self.settingsView, 0, 0, 1, 1)
        self.settingsStack.addWidget(self.mainPage)
        self.systemPage = QtWidgets.QWidget()
        self.systemPage.setStyleSheet("")
        self.systemPage.setObjectName("systemPage")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.systemPage)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.systemPage)
        self.scrollArea.setStyleSheet("QWidget\n"
"{\n"
"    background-color: #232629;\n"
"}")
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 777, 408))
        self.scrollAreaWidgetContents.setStyleSheet("")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setHorizontalSpacing(14)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(25)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.swapScannersBtn = TouchButton(self.scrollAreaWidgetContents)
        self.swapScannersBtn.setMinimumSize(QtCore.QSize(64, 64))
        self.swapScannersBtn.setMaximumSize(QtCore.QSize(64, 64))
        self.swapScannersBtn.setStyleSheet("background-color: transparent;\n"
"border: 0;")
        self.swapScannersBtn.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/Icons/Icons/Swap_Finished.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.swapScannersBtn.setIcon(icon4)
        self.swapScannersBtn.setIconSize(QtCore.QSize(64, 64))
        self.swapScannersBtn.setObjectName("swapScannersBtn")
        self.gridLayout_3.addWidget(self.swapScannersBtn, 0, 3, 2, 1)
        self.secondaryLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        self.secondaryLabel.setFont(font)
        self.secondaryLabel.setObjectName("secondaryLabel")
        self.gridLayout_3.addWidget(self.secondaryLabel, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 0, 2, 1, 1)
        self.primaryLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        self.primaryLabel.setFont(font)
        self.primaryLabel.setObjectName("primaryLabel")
        self.gridLayout_3.addWidget(self.primaryLabel, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(25)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_3)
        self.line = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        spacerItem3 = QtWidgets.QSpacerItem(20, 253, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem3)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.settingsStack.addWidget(self.systemPage)
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.page)
        self.scrollArea_2.setStyleSheet("QWidget\n"
"{\n"
"    background-color: #232629;\n"
"}")
        self.scrollArea_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 777, 408))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.expDateSpinBox = TouchSpinBox(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        self.expDateSpinBox.setFont(font)
        self.expDateSpinBox.setMinimum(1)
        self.expDateSpinBox.setMaximum(25)
        self.expDateSpinBox.setObjectName("expDateSpinBox")
        self.gridLayout.addWidget(self.expDateSpinBox, 2, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 2, 1, 1)
        self.shelfTimeCheckBox = TouchCheckbox(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        self.shelfTimeCheckBox.setFont(font)
        self.shelfTimeCheckBox.setObjectName("shelfTimeCheckBox")
        self.gridLayout.addWidget(self.shelfTimeCheckBox, 0, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 2, 1, 1)
        self.expDateCheckBox = TouchCheckbox(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        self.expDateCheckBox.setFont(font)
        self.expDateCheckBox.setObjectName("expDateCheckBox")
        self.gridLayout.addWidget(self.expDateCheckBox, 2, 0, 1, 1)
        self.usageRateCheckBox = TouchCheckbox(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        self.usageRateCheckBox.setFont(font)
        self.usageRateCheckBox.setObjectName("usageRateCheckBox")
        self.gridLayout.addWidget(self.usageRateCheckBox, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)
        self.usageRateSpinBox = TouchSpinBox(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        self.usageRateSpinBox.setFont(font)
        self.usageRateSpinBox.setMinimum(1)
        self.usageRateSpinBox.setMaximum(25)
        self.usageRateSpinBox.setObjectName("usageRateSpinBox")
        self.gridLayout.addWidget(self.usageRateSpinBox, 1, 3, 1, 1)
        self.shelfTimeSpinBox = TouchSpinBox(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        self.shelfTimeSpinBox.setFont(font)
        self.shelfTimeSpinBox.setMinimum(1)
        self.shelfTimeSpinBox.setMaximum(25)
        self.shelfTimeSpinBox.setProperty("value", 1)
        self.shelfTimeSpinBox.setObjectName("shelfTimeSpinBox")
        self.gridLayout.addWidget(self.shelfTimeSpinBox, 0, 3, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 0, 4, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 2, 4, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 1, 4, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 0, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 1, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem6, 2, 1, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout)
        self.line_2 = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_6.addWidget(self.line_2)
        spacerItem7 = QtWidgets.QSpacerItem(20, 203, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem7)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_5.addWidget(self.scrollArea_2)
        self.settingsStack.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.settingsStack.addWidget(self.page_2)
        self.verticalLayout_3.addWidget(self.settingsStack)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.retranslateUi(SettingsWindow)
        self.settingsStack.setCurrentIndex(2)
        self.settingsView.setCurrentRow(-1)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "Smart Shop"))
        __sortingEnabled = self.settingsView.isSortingEnabled()
        self.settingsView.setSortingEnabled(False)
        item = self.settingsView.item(0)
        item.setText(_translate("SettingsWindow", "System"))
        item = self.settingsView.item(1)
        item.setText(_translate("SettingsWindow", "Algorithm"))
        self.settingsView.setSortingEnabled(__sortingEnabled)
        self.label_2.setText(_translate("SettingsWindow", "Primary:"))
        self.secondaryLabel.setText(_translate("SettingsWindow", "5"))
        self.primaryLabel.setText(_translate("SettingsWindow", "4"))
        self.label_3.setText(_translate("SettingsWindow", "Secondary:"))
        self.label_6.setText(_translate("SettingsWindow", "Threshold:"))
        self.shelfTimeCheckBox.setText(_translate("SettingsWindow", "Shelf Time Algorithm"))
        self.label_7.setText(_translate("SettingsWindow", "Threshold:"))
        self.expDateCheckBox.setText(_translate("SettingsWindow", "Expiration Date Algorithm"))
        self.usageRateCheckBox.setText(_translate("SettingsWindow", "Usage Rate Algorithm"))
        self.label.setText(_translate("SettingsWindow", "Threshold:"))
        self.label_8.setText(_translate("SettingsWindow", "days"))
        self.label_10.setText(_translate("SettingsWindow", "days"))
        self.label_9.setText(_translate("SettingsWindow", "days"))

from Widgets.touchButton import TouchButton
from Widgets.touchCheckbox import TouchCheckbox
from Widgets.touchSpinBox import TouchSpinBox
import Resource_BY_rc
import style_rc
