from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Windows.centralWindow import *
from Windows import favoriteWindow_ui
from Util import constants, scroller
from Util.enums import *

class FavoriteWindow(QWidget, favoriteWindow_ui.Ui_FavoriteWindow):
    def __init__(self, parent=None):
        super(FavoriteWindow, self).__init__(parent)
        self.setupUi(self)

        self.favoritesTabModel = QStandardItemModel(4, 5, self)

        self.favoritesTabModel.setItem(0, 0, QStandardItem("Rawr"))
        self.favoritesTabModel.setItem(0, 1, QStandardItem("Really Long String of Words"))
        self.favoritesTabModel.setItem(0, 2, QStandardItem("Really Long"))
        self.favoritesTabModel.setItem(0, 3, QStandardItem("POPTARTS STRAWBERRY"))
        self.favoritesTabModel.setItem(1, 0, QStandardItem("Rawr"))
        self.favoritesTabModel.setItem(1, 1, QStandardItem("OOOOOOOOOO OOOOOOOOOO"))
        self.favoritesTabModel.setItem(1, 2, QStandardItem("OOOOOOOOOO OOOOOOOOO"))
        self.favoritesTabModel.setItem(1, 3, QStandardItem("OOOOOOOOO OOOOOOOO"))
        self.favoritesTabModel.setItem(1, 4, QStandardItem("OOOOOOOO OOOOOOO"))

        self.favoritesTableView.setModel(self.favoritesTabModel)
        scroller.setupScrolling(self.favoritesTableView)

        # Setup a tab
        self.testTab = QWidget(self.categoryTabWidget)
        self.horizontalLayout_10 = QHBoxLayout(self.testTab)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)

        self.testTabList = QListView(self.testTab)
        font = QFont()
        font.setPointSize(21)
        self.testTabList.setFont(font)
        self.testTabList.setFrameShape(QFrame.NoFrame)
        self.testTabList.setFrameShadow(QFrame.Plain)
        self.testTabList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.testTabList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.testTabList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.testTabList.setDragDropMode(QAbstractItemView.DragDrop)
        self.testTabList.setDefaultDropAction(Qt.ActionMask)
        self.testTabList.setAlternatingRowColors(True)
        self.testTabList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.testTabList.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.testTabList.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.horizontalLayout_10.addWidget(self.testTabList)

        self.categoryTabWidget.addTab(self.testTab, 'Test')

        self.stringList = QStringListModel(self)
        self.stringList.setStringList(['One', 'Two', 'Three', 'Four', 'Five'])

        self.testTabList.setModel(self.stringList)

    @pyqtSlot()
    def showEvent(self, event):
        self.centralWindow.primaryScanner.barcodeReceived.connect(self.primaryScanner_barcodeReceived)
        self.centralWindow.secondaryScanner.barcodeReceived.connect(self.secondaryScanner_barcodeReceived)
        print('This widget is being shown. Handle anything necessary. Favorite Window')

    @pyqtSlot()
    def hideEvent(self, event):
        self.centralWindow.primaryScanner.barcodeReceived.disconnect(self.primaryScanner_barcodeReceived)
        self.centralWindow.secondaryScanner.barcodeReceived.disconnect(self.secondaryScanner_barcodeReceived)
        print('This widget is being hidden. Handle anything necessary. Favorite Window')

    @pyqtSlot()
    def on_backBtn_clicked(self):
        self.parent().setCurrentIndex(WindowType.Main)

    @pyqtSlot()
    def on_homeBtn_clicked(self):
        self.parent().setCurrentIndex(WindowType.Main)

    @pyqtSlot(str)
    def primaryScanner_barcodeReceived(self, barcode):
        print("Fav: Primary barcode scanner got: %s" % barcode)
        # TODO Send the barcode scanner information to be processed

    @pyqtSlot(str)
    def secondaryScanner_barcodeReceived(self, barcode):
        print("Fav: Secondary barcode scanner got: %s" % barcode)
        # TODO Send the barcode scanner information to be processed
