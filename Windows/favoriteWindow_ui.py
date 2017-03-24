# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'favoriteWindow.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FavoriteWindow(object):
    def setupUi(self, FavoriteWindow):
        FavoriteWindow.setObjectName("FavoriteWindow")
        FavoriteWindow.setWindowModality(QtCore.Qt.NonModal)
        FavoriteWindow.resize(800, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FavoriteWindow.sizePolicy().hasHeightForWidth())
        FavoriteWindow.setSizePolicy(sizePolicy)
        FavoriteWindow.setMaximumSize(QtCore.QSize(855, 661))
        font = QtGui.QFont()
        font.setPointSize(15)
        FavoriteWindow.setFont(font)
        FavoriteWindow.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        FavoriteWindow.setProperty("dockNestingEnabled", False)
        FavoriteWindow.setProperty("unifiedTitleAndToolBarOnMac", False)
        self.gridLayout = QtWidgets.QGridLayout(FavoriteWindow)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(5, -1, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.backBtn = QtWidgets.QPushButton(FavoriteWindow)
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
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 2, 1)
        spacerItem1 = QtWidgets.QSpacerItem(260, 63, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 2, 1)
        self.homeBtn = QtWidgets.QPushButton(FavoriteWindow)
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
        self.gridLayout.addWidget(self.homeBtn, 0, 1, 2, 1)
        self.tabWidget = QtWidgets.QTabWidget(FavoriteWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setKerning(True)
        self.tabWidget.setFont(font)
        self.tabWidget.setAcceptDrops(True)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidgetPage1 = QtWidgets.QWidget()
        self.tabWidgetPage1.setObjectName("tabWidgetPage1")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tabWidgetPage1)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tableView = TileView(self.tabWidgetPage1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.tableView.setFont(font)
        self.tableView.setStyleSheet("")
        self.tableView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableView.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableView.setLineWidth(0)
        self.tableView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableView.setAutoScroll(True)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setDragEnabled(True)
        self.tableView.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.tableView.setDefaultDropAction(QtCore.Qt.ActionMask)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.tableView.setTextElideMode(QtCore.Qt.ElideRight)
        self.tableView.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableView.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableView.setShowGrid(True)
        self.tableView.setWordWrap(True)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setVisible(False)
        self.tableView.horizontalHeader().setDefaultSectionSize(154)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.verticalHeader().setDefaultSectionSize(90)
        self.gridLayout_4.addWidget(self.tableView, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabWidgetPage1, "")
        self.tabWidgetPage2 = QtWidgets.QWidget()
        self.tabWidgetPage2.setObjectName("tabWidgetPage2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tabWidgetPage2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_8 = QtWidgets.QLabel(self.tabWidgetPage2)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setWordWrap(True)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 1, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.tabWidgetPage2)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setWordWrap(True)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.pushButton_13 = QtWidgets.QPushButton(self.tabWidgetPage2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_13.sizePolicy().hasHeightForWidth())
        self.pushButton_13.setSizePolicy(sizePolicy)
        self.pushButton_13.setObjectName("pushButton_13")
        self.gridLayout_2.addWidget(self.pushButton_13, 1, 1, 1, 1)
        self.toolButton_8 = QtWidgets.QToolButton(self.tabWidgetPage2)
        self.toolButton_8.setObjectName("toolButton_8")
        self.gridLayout_2.addWidget(self.toolButton_8, 0, 1, 1, 1)
        self.tabWidget.addTab(self.tabWidgetPage2, "")
        self.tabWidgetPage3 = QtWidgets.QWidget()
        self.tabWidgetPage3.setObjectName("tabWidgetPage3")
        self.tabWidget.addTab(self.tabWidgetPage3, "")
        self.tabWidgetPage4 = QtWidgets.QWidget()
        self.tabWidgetPage4.setObjectName("tabWidgetPage4")
        self.tabWidget.addTab(self.tabWidgetPage4, "")
        self.tabWidgetPage5 = QtWidgets.QWidget()
        self.tabWidgetPage5.setObjectName("tabWidgetPage5")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tabWidgetPage5)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.listWidget = QtWidgets.QListWidget(self.tabWidgetPage5)
        font = QtGui.QFont()
        font.setPointSize(19)
        self.listWidget.setFont(font)
        self.listWidget.setStyleSheet("")
        self.listWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.listWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidget.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listWidget.setDefaultDropAction(QtCore.Qt.ActionMask)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.listWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.listWidget.setFlow(QtWidgets.QListView.TopToBottom)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.gridLayout_3.addWidget(self.listWidget, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabWidgetPage5, "")
        self.tabWidgetPage6 = QtWidgets.QWidget()
        self.tabWidgetPage6.setObjectName("tabWidgetPage6")
        self.tabWidget.addTab(self.tabWidgetPage6, "")
        self.gridLayout.addWidget(self.tabWidget, 2, 0, 1, 3)
        self.floatingBtnWidget = QtWidgets.QWidget(FavoriteWindow)
        self.floatingBtnWidget.setStyleSheet("background-color: rgba(0,0,0,0);")
        self.floatingBtnWidget.setObjectName("floatingBtnWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.floatingBtnWidget)
        self.horizontalLayout.setContentsMargins(0, 3, 0, 6)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.floatingBtnWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMinimumSize(QtCore.QSize(48, 48))
        self.pushButton_2.setMaximumSize(QtCore.QSize(48, 48))
        self.pushButton_2.setStyleSheet("background-color: transparent; border: 0;")
        self.pushButton_2.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Icons/Icons/GreenPlusIcon_Finished.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon2)
        self.pushButton_2.setIconSize(QtCore.QSize(48, 48))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.floatingBtnWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(48, 48))
        self.pushButton.setMaximumSize(QtCore.QSize(48, 48))
        self.pushButton.setStyleSheet("background-color: transparent;\n"
"border: 0;")
        self.pushButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Icons/Icons/RedMinusIcon_Finished.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon3)
        self.pushButton.setIconSize(QtCore.QSize(48, 48))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.gridLayout.addWidget(self.floatingBtnWidget, 3, 1, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.pushButton_4 = QtWidgets.QPushButton(FavoriteWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setMinimumSize(QtCore.QSize(48, 48))
        self.pushButton_4.setMaximumSize(QtCore.QSize(48, 48))
        self.pushButton_4.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.pushButton_4.setStyleSheet("background-color: transparent;\n"
"border: 0;r")
        self.pushButton_4.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/Icons/Icons/EditIcon_Finished.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon4)
        self.pushButton_4.setIconSize(QtCore.QSize(48, 48))
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_3.addWidget(self.pushButton_4)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.gridLayout.addLayout(self.horizontalLayout_3, 3, 2, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)

        self.retranslateUi(FavoriteWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(FavoriteWindow)

    def retranslateUi(self, FavoriteWindow):
        _translate = QtCore.QCoreApplication.translate
        FavoriteWindow.setWindowTitle(_translate("FavoriteWindow", "Smart Shop"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage1), _translate("FavoriteWindow", "Favorite\'s"))
        self.label_8.setText(_translate("FavoriteWindow", "TextLabel"))
        self.label_7.setText(_translate("FavoriteWindow", "TextLabel"))
        self.pushButton_13.setText(_translate("FavoriteWindow", "PushButton"))
        self.toolButton_8.setText(_translate("FavoriteWindow", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage2), _translate("FavoriteWindow", "Produce"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage3), _translate("FavoriteWindow", "Dairy"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage4), _translate("FavoriteWindow", "Meat"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("FavoriteWindow", "New Item"))
        item = self.listWidget.item(1)
        item.setText(_translate("FavoriteWindow", "New Item"))
        item = self.listWidget.item(2)
        item.setText(_translate("FavoriteWindow", "New Item"))
        item = self.listWidget.item(3)
        item.setText(_translate("FavoriteWindow", "New Item"))
        item = self.listWidget.item(4)
        item.setText(_translate("FavoriteWindow", "New Item"))
        item = self.listWidget.item(5)
        item.setText(_translate("FavoriteWindow", "New Item"))
        item = self.listWidget.item(6)
        item.setText(_translate("FavoriteWindow", "New Item"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage5), _translate("FavoriteWindow", "Beverages"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage6), _translate("FavoriteWindow", "Other"))

from Widgets.tileView import TileView
import Resource_BY_rc
import style_rc
