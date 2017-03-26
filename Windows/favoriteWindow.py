from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Windows.centralWindow import *
from Windows import favoriteWindow_ui
from Util import constants, scroller
from Util.enums import *

class CategoryTab():
    __slots__ = ['widget', 'horizontalLayout', 'listView']
    def __init__(self, widget = None, horizontalLayout = None, listView = None):
        self.widget = widget
        self.horizontalLayout = horizontalLayout
        self.listView = listView

class FavoriteWindow(QWidget, favoriteWindow_ui.Ui_FavoriteWindow):
    def __init__(self, centralWindow, config, dbManager, parent=None):
        super(FavoriteWindow, self).__init__(parent)
        self.setupUi(self)

        self.centralWindow = centralWindow
        self.config = config
        self.dbManager = dbManager

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

        # Create an empty tabDict which will contain a dictionary for each tab in the window, query all categories and
        # add each tab to the window
        self.tabDict = {}
        self.categories = self.dbManager.GetCategories(True)
        for category in self.categories:
            self.addTab(category['id'], category['name'])

    def addTab(self, id, name):
        newTab = CategoryTab(QWidget(self.categoryTabWidget))
        newTab.horizontalLayout = QHBoxLayout(newTab.widget)
        newTab.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        # Create list view for category and with the appropiate settings
        newTab.listView = QListView(newTab.widget)
        font = QFont()
        font.setPointSize(21)
        newTab.listView.setFont(font)
        newTab.listView.setFrameShape(QFrame.NoFrame)
        newTab.listView.setFrameShadow(QFrame.Plain)
        newTab.listView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        newTab.listView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        newTab.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        newTab.listView.setDragDropMode(QAbstractItemView.DragDrop)
        newTab.listView.setDefaultDropAction(Qt.ActionMask)
        newTab.listView.setAlternatingRowColors(True)
        newTab.listView.setSelectionMode(QAbstractItemView.MultiSelection)
        newTab.listView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        newTab.listView.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        newTab.horizontalLayout.addWidget(newTab.listView)

        # Add tab to tab widget as well as the tabDict variable
        self.categoryTabWidget.addTab(newTab.widget, name)
        self.tabDict[id] = newTab

        # Set list view to have model to display items
        self.stringList = QStringListModel(self)
        self.stringList.setStringList(['One', 'Two', 'Three', 'Four', 'Five'])

        newTab.listView.setModel(self.stringList)

    @pyqtSlot()
    def showEvent(self, event):
        self.centralWindow.primaryScanner.barcodeReceived.connect(self.primaryScanner_barcodeReceived)
        self.centralWindow.secondaryScanner.barcodeReceived.connect(self.secondaryScanner_barcodeReceived)

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
