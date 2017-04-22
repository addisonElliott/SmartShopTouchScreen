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
    def __init__(self, centralWindow, config, dbManager, barcodeManager, parent=None):
        super(FavoriteWindow, self).__init__(parent)
        self.setupUi(self)

        self.centralWindow = centralWindow
        self.config = config
        self.dbManager = dbManager
        self.barcodeManager = barcodeManager

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

        # Enable the add and remove button because they are only shown when items are selected on the current tab
        self.addBtn.setEnabled(False)
        self.removeBtn.setEnabled(False)

        # TODO Allow user to scroll through categories tab widget with their finger.
        # TODO Integrate drag/drop functions to allow items to be transferred from one category to another
        # TODO Create category edit menu to edit information regarding the category. Allow reordering of categories

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
        newTab.listView.verticalHeader().setVisible(False)
        newTab.listView.verticalHeader().setDefaultSectionSize(45)
        newTab.listView.setSelectionBehavior(QAbstractItemView.SelectRows)
        newTab.listView.setSortingEnabled(True)
        newTab.listView.sortByColumn(0, Qt.AscendingOrder)
        newTab.horizontalLayout.addWidget(newTab.listView)

        newTab.listModel = SqlTableModel(self.dbManager.connection, 'inventory', 'name', Qt.AscendingOrder, 'category=%s',
                                         (id,), ('item', 'name', 'qty'), (1, 2), ('Name', 'Qty'))
        newTab.listView.setModel(newTab.listModel)
        newTab.listView.selectionModel().selectionChanged.connect(self.selectItem)

        # Set the name column to stretch to fill the area while the qty column is resized to contents
        newTab.listView.horizontalHeader().setStretchLastSection(False)
        newTab.listView.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        newTab.listView.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        # Setup kinetic scrolling on category listView
        scroller.setupScrolling(newTab.listView)

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
        # On show, set the current tab to favorite's, clear selections for each tab and set sort back to default
        self.categoryTabWidget.setCurrentIndex(0)
        self.favoritesTabModel.select()
        self.favoritesTableView.selectionModel().clearSelection()

        # Create an empty tabDict which will contain a dictionary for each tab in the window
        self.tabDict = {}

        # Loop through every category and remove it except for the favorite's tab (index 0)
        # Keep pulling items from index 1 until there is no index 1
        for x in range(1, self.categoryTabWidget.count()):
            widget = self.categoryTabWidget.widget(1)
            self.categoryTabWidget.removeTab(1) # Keep removing the next tab after favorite's window and they will all be gone
            widget.deleteLater()

        # Query all categories and add each tab to the window
        self.categories = self.dbManager.GetCategories(True)
        for category in self.categories:
            self.addTab(category['id'], category['name'])

        # On show, set the current tab to favorite's, clear selections for each tab and set sort back to default
        for id, category in self.tabDict.items():
            category.listView.selectionModel().clearSelection()
            category.listView.sortByColumn(0, Qt.AscendingOrder)

    @pyqtSlot()
    def hideEvent(self, event):
        pass

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
            records = self.favoritesTabModel.getSelectedRecords(self.currentSelectionModel.selectedRows())
        else:
            # Get category ID by looking up index in categories variable
            categoryID = self.categories[index - 1]['id']

            # Get selection model based on category ID
            tabCategory = self.tabDict[categoryID]
            records = tabCategory.listModel.getSelectedRecords(self.currentSelectionModel.selectedRows())

        if longPressed:
            # Only take the first record and do this to it
            record = records[0]
            expirationDate, quantity, callbackFunction, callbackParam = \
                            self.barcodeManager.DisplayExpirationBox(record['name'])
            cachedItem = {'item': record['item'], 'pkg_qty': 1}

            self.dbManager.UpdateItemInDatabase(cachedItem, expirationDate, quantity)

            if callbackFunction and callbackParam:
                callbackFunction(callbackParam)
        else:
            # Update each record that is currently selected
            for record in records:
                # Do not give a new expiration date and update the quantity by one
                cachedItem = {'item': record['item'], 'pkg_qty': 1}
                self.dbManager.UpdateItemInDatabase(cachedItem, None, 1)

        # Clear the current selection since it has been handled and refresh the lists since changes were made to database
        self.currentSelectionModel.clearSelection()
        self.refreshLists()

    @pyqtSlot(bool, bool)
    def on_removeBtn_clicked(self, checked, longPressed):
        index = self.categoryTabWidget.currentIndex()

        # Handle favorite's tab versus category list
        if index == 0:
            records = self.favoritesTabModel.getSelectedRecords(self.currentSelectionModel.selectedRows())
        else:
            # Get category ID by looking up index in categories variable
            categoryID = self.categories[index - 1]['id']

            # Get selection model based on category ID
            tabCategory = self.tabDict[categoryID]
            records = tabCategory.listModel.getSelectedRecords(self.currentSelectionModel.selectedRows())

        if longPressed:
            # Only take the first record and do this to it
            record = records[0]
            returnResult, quantity, callbackFunction, callbackParam = \
                self.barcodeManager.displayCheckOutBox(record['name'])

            # Only decrement the item if the user clicked accept
            if returnResult:
                self.dbManager.DecrementQuantityForItem(record['item'], quantity)

            if callbackFunction and callbackParam:
                callbackFunction(callbackParam)
        else:
            # Update each record that is currently selected
            for record in records:
                self.dbManager.DecrementQuantityForItem(record['item'], 1)

        # Clear the current selection since it has been handled and refresh the lists since changes were made to database
        self.currentSelectionModel.clearSelection()
        self.refreshLists()

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

    @pyqtSlot(bool, bool)
    def on_shoppingListAddBtn_clicked(self, checked, longPressed):
        # If the current selection model has nothing selected, then do nothing
        if not self.currentSelectionModel.hasSelection():
            return

        index = self.categoryTabWidget.currentIndex()

        # Handle favorite's tab versus category list
        if index == 0:
            records = self.favoritesTabModel.getSelectedRecords(self.currentSelectionModel.selectedRows())
        else:
            # Get category ID by looking up index in categories variable
            categoryID = self.categories[index - 1]['id']

            # Get selection model based on category ID
            tabCategory = self.tabDict[categoryID]
            records = tabCategory.listModel.getSelectedRecords(self.currentSelectionModel.selectedRows())

        itemList = tuple(record['item'] for record in records)
        self.dbManager.setRequiredItems(itemList)
        self.currentSelectionModel.clearSelection()

    def refreshLists(self):
        # Refresh the favorite's tile view
        self.favoritesTabModel.select()

        # Loop through each category and refresh each of the lists
        for id, category in self.tabDict.items():
            category.listModel.select()

    @pyqtSlot(str)
    def primaryScanner_barcodeReceived(self, barcode):
        self.refreshLists()

    @pyqtSlot(str)
    def secondaryScanner_barcodeReceived(self, barcode):
        print("Secondary barcode scanner got: %s" % barcode)
        self.refreshLists()