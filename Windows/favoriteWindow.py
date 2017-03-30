from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Windows.manualAddDialog import *

from Windows.centralWindow import *
from Windows import favoriteWindow_ui
from Util import constants, scroller
from Util.enums import *
from Util.SqlTableModel import *
from Util.SqlTileTableModel import *
import logging

logger = logging.getLogger(__name__)

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

        self.favoritesTabModel = SqlTileTableModel(self.dbManager.connection, 'inventory', 'favorites_index',
                                                    Qt.AscendingOrder, 'favorites_index IS NOT NULL', (1,),
                                                    ('item', 'name', 'qty'), 5, 1)

        # Set Favorite's View to have model
        self.favoritesTableView.setModel(self.favoritesTabModel)
        # Setup kinetic scrolling on favorite's table view (can use touchscreen to flick and scroll like on phones)
        scroller.setupScrolling(self.favoritesTableView)
        # Connect selectItem function to the selectionChanged signal that is triggered when an item is deselected or
        # selected
        self.favoritesTableView.selectionModel().selectionChanged.connect(self.selectItem)
        # Set the current selection model to be the favorite's tab selection model
        self.currentSelectionModel = self.favoritesTableView.selectionModel()

        # Create an empty tabDict which will contain a dictionary for each tab in the window, query all categories and
        # add each tab to the window
        self.tabDict = {}
        self.categories = self.dbManager.GetCategories(True)
        for category in self.categories:
            self.addTab(category['id'], category['name'])

        # Enable the add and remove button because they are only shown when items are selected on the current tab
        self.addBtn.setEnabled(False)
        self.removeBtn.setEnabled(False)

    def addTab(self, id, name):
        newTab = CategoryTab(QWidget(self.categoryTabWidget))
        newTab.horizontalLayout = QHBoxLayout(newTab.widget)
        newTab.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        # Create list view for category and with the appropiate settings
        newTab.listView = QTableView(newTab.widget)
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
                                         (id,), ('item', 'name', 'qty'), (1, 2), ('Name', 'Qty'))
        newTab.listView.setModel(newTab.listModel)
        newTab.listView.selectionModel().selectionChanged.connect(self.selectItem)

        # Set the name column to stretch to fill the area while the qty column is resized to contents
        newTab.listView.horizontalHeader().setStretchLastSection(False)
        newTab.listView.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        newTab.listView.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        # Add tab to tab widget as well as the tabDict variable
        self.categoryTabWidget.addTab(newTab.widget, name)
        self.tabDict[id] = newTab

    @pyqtSlot()
    def selectItem(self):
        hasSelection = not self.sender().selection().isEmpty()
        self.addBtn.setEnabled(hasSelection)
        self.removeBtn.setEnabled(hasSelection)

    @pyqtSlot(int)
    def on_categoryTabWidget_currentChanged(self, index):
        # If the index is zero, this get the selection model for the favorite's tab, otherwise, get the selection model
        # for the indexed tab.
        if index == 0:
            self.currentSelectionModel = self.favoritesTableView.selectionModel()
        else:
            # Get category ID by looking up index in categories variable
            categoryID = self.categories[index - 1]['id']

            # Get selection model based on category ID
            self.currentSelectionModel = self.tabDict[categoryID].listView.selectionModel()

        hasSelection = not self.currentSelectionModel.selection().isEmpty()
        self.addBtn.setEnabled(hasSelection)
        self.removeBtn.setEnabled(hasSelection)

    @pyqtSlot()
    def showEvent(self, event):
        self.centralWindow.primaryScanner.barcodeReceived.connect(self.primaryScanner_barcodeReceived)
        self.centralWindow.secondaryScanner.barcodeReceived.connect(self.secondaryScanner_barcodeReceived)

    @pyqtSlot()
    def hideEvent(self, event):
        self.centralWindow.primaryScanner.barcodeReceived.disconnect(self.primaryScanner_barcodeReceived)
        self.centralWindow.secondaryScanner.barcodeReceived.disconnect(self.secondaryScanner_barcodeReceived)

    @pyqtSlot(bool, bool)
    def on_backBtn_clicked(self, checked, longPressed):
        self.parent().setCurrentIndex(WindowType.Main)

    @pyqtSlot(bool, bool)
    def on_homeBtn_clicked(self, checked, longPressed):
        self.parent().setCurrentIndex(WindowType.Main)

    @pyqtSlot(bool, bool)
    def on_addBtn_clicked(self, checked, longPressed):
        index = self.categoryTabWidget.currentIndex()

        # Handle favorite's tab versus category list
        if index == 0:
            selectionModel = self.favoritesTableView.selectionModel()
            records = self.favoritesTabModel.getSelectedRecords(self.currentSelectionModel.selectedIndexes())
        else:
            # Get category ID by looking up index in categories variable
            categoryID = self.categories[index - 1]['id']

            # Get selection model based on category ID
            tabCategory = self.tabDict[categoryID]
            selectionModel = tabCategory.listView.selectionModel()
            records = tabCategory.listModel.getSelectedRecords(self.currentSelectionModel.selectedIndexes())

        if longPressed:
            # Open up the Expiration Dialog for each item, query information
            # DeSelect all items currently selected
            i = 4
        else:
            # Add one to each of the items selected
            # DeSelect all items currently selected
            i = 5

    @pyqtSlot(bool, bool)
    def on_removeBtn_clicked(self, checked, longPressed):
        index = self.categoryTabWidget.currentIndex()

        # Handle favorite's tab versus category list
        if index == 0:
            selectionModel = self.favoritesTableView.selectionModel()
            records = self.favoritesTabModel.getSelectedRecords(self.currentSelectionModel.selectedIndexes())
        else:
            # Get category ID by looking up index in categories variable
            categoryID = self.categories[index - 1]['id']

            # Get selection model based on category ID
            tabCategory = self.tabDict[categoryID]
            selectionModel = tabCategory.listView.selectionModel()
            records = tabCategory.listModel.getSelectedRecords(self.currentSelectionModel.selectedIndexes())

        if longPressed:
            i = 4
            # Bring up a box for each one that asks how many to remove
            # DeSelect all items currently selected
        else:
            # Subtract one from each of the items selected
            # DeSelect all items currently selected
            i = 5

    @pyqtSlot(bool, bool)
    def on_listAddBtn_clicked(self, checked, longPressed):
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
        logger.info("Primary barcode scanned in Favorite's Menu: Note, this does nothing. You must be on the main menu")

    @pyqtSlot(str)
    def secondaryScanner_barcodeReceived(self, barcode):
        logger.info("Secondary barcode scanned in Favorite's Menu: Note, this does nothing. You must be on the main menu")
