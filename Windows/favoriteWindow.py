from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Windows.manualAddDialog import *

from Windows.centralWindow import *
from Windows import favoriteWindow_ui
from Util import constants, scroller
from Util.enums import *
from Util.SqlTableModel import *

class CategoryTab():
    __slots__ = ['widget', 'horizontalLayout', 'listView', 'listModel']
    def __init__(self, widget = None, horizontalLayout = None, listView = None, listModel = None):
        self.widget = widget
        self.horizontalLayout = horizontalLayout
        self.listView = listView
        self.listModel = listModel

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

        newTab.listModel = SqlTableModel(self.dbManager.connection, 'inventory', 'name', Qt.AscendingOrder, 'category=%s',
                                         (id,), ('name',))
        newTab.listView.setModel(newTab.listModel)

        # Add tab to tab widget as well as the tabDict variable
        self.categoryTabWidget.addTab(newTab.widget, name)
        self.tabDict[id] = newTab

    @pyqtSlot()
    def showEvent(self, event):
        self.centralWindow.primaryScanner.barcodeReceived.connect(self.primaryScanner_barcodeReceived)
        self.centralWindow.secondaryScanner.barcodeReceived.connect(self.secondaryScanner_barcodeReceived)

    @pyqtSlot()
    def hideEvent(self, event):
        self.centralWindow.primaryScanner.barcodeReceived.disconnect(self.primaryScanner_barcodeReceived)
        self.centralWindow.secondaryScanner.barcodeReceived.disconnect(self.secondaryScanner_barcodeReceived)

    @pyqtSlot()
    def on_backBtn_clicked(self):
        self.parent().setCurrentIndex(WindowType.Main)

    @pyqtSlot()
    def on_homeBtn_clicked(self):
        self.parent().setCurrentIndex(WindowType.Main)

    @pyqtSlot()
    def on_listAddBtn_clicked(self):
        # Create a ManualAddDialog, pass the configuration variables such as config, dbManager and categories
        # The category combo box in the dialog will be set to the currently selected tab in the Favorite's Menu. However,
        # if the currently selected tab is the favorite's, then it will default to the first category
        dialog = ManualAddDialog(self.config, self.dbManager, self.categories,
                                 max(self.categoryTabWidget.currentIndex() - 1, 0), self)

        # Run the dialog, if successfully completed, then add new item to category
        if dialog.exec():
            item = {}

            catComboInd = dialog.categoryComboBox.currentIndex()
            item['name'] = dialog.nameEdit.text()
            item['category'] = dialog.categories[catComboInd]['id']

            if dialog.favoritesCheckbox.isChecked():
                index = self.dbManager.GetFavoritesCount()
                if index is None: # If the values are all NULL, set to 0
                    index = 0

                index += 1 # Increment index by 1
                item['favoritesIndex'] = index

            self.dbManager.AddItemToInventory(item)

            # If the category currently exists (check tabDict for the id), then refresh the list model by calling select
            # Otherwise, the category will be added later on and it will automatically be updated on creation
            if item['category'] in self.tabDict:
                self.tabDict[item['category']].listModel.select()

        # If the categories list that was sent to the dialog is not the same when finishing, that means a new category
        # was added and the new category list was queried. Update the categories variable in FavoriteWindow and add the
        # appropiate tabs
        if self.categories is not dialog.categories:
            self.categories = dialog.categories

            for category in self.categories:
                if not category['id'] in self.tabDict:
                    self.addTab(category['id'], category['name'])

    @pyqtSlot(str)
    def primaryScanner_barcodeReceived(self, barcode):
        print("Fav: Primary barcode scanner got: %s" % barcode)
        # TODO Send the barcode scanner information to be processed

    @pyqtSlot(str)
    def secondaryScanner_barcodeReceived(self, barcode):
        print("Fav: Secondary barcode scanner got: %s" % barcode)
        # TODO Send the barcode scanner information to be processed
