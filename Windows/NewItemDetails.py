from Windows import NewItemDetails_ui
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Util import constants
from Util import scroller
from datetime import datetime
from Windows.virtualKeyboard import *
from Util.SqlTableModel import *
import logging

logger = logging.getLogger(__name__)


class NewItemDetails(QDialog, NewItemDetails_ui.Ui_NewItemDetails):
    newCategoryText = 'newCategory'
    pendingCategoryText = 'pendingCategory'

    def __init__(self, dbManager, config, categories, parent=None):
        super(NewItemDetails, self).__init__(parent)
        self.setupUi(self)

        self.dbManager = dbManager
        self.config = config
        self.categories = categories
        self.pending_category = None

        # Remove title bar
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)

        self.itemNameModel = SqlTableModel(self.dbManager.connection, columnSortName='rank',
                                        columnSortOrder=Qt.DescendingOrder,
                                        customQuery='SELECT item, name, CASE\n'
                                        'WHEN name LIKE %s THEN 3\n'
                                        'WHEN name ILIKE %s THEN 2\n'
                                        'WHEN name LIKE %s THEN 1\n'
                                        'ELSE 0 END AS rank FROM inventory\n'
                                        'WHERE name ILIKE %s', filterArgs=('%', '%%', '%', '%%'),
                                        displayColumnMapping=(1,), limitCount = 10, hideItems=True)
        self.itemName_textBox.autocompleteModel = self.itemNameModel
        self.itemName_textBox.autocompleteUpdateCallback = self.itemName_updateSuggestions

        scroller.setupScrolling(self.category_combo.view())
        # Set the combobox view to scroll per pixel so the kinetic scrolling via touchscreen isnt ridiculously fast
        self.category_combo.view().setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # Disabling mouse tracking means that when you first use touchscreen to scroll through items, then it wont
        # select that item
        self.category_combo.view().setMouseTracking(False)
        self.updateCategories()

        scroller.setupScrolling(self.itemQty_combo.view())
        self.itemQty_combo.view().setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.itemQty_combo.view().setMouseTracking(False)
        for q in range(1, 51):
            self.itemQty_combo.addItem(str(q))

        scroller.setupScrolling(self.pkgQty_combo.view())
        self.pkgQty_combo.view().setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.pkgQty_combo.view().setMouseTracking(False)
        for q in range(1, 51):
            self.pkgQty_combo.addItem(str(q))

        scroller.setupScrolling(self.month_combo.view())
        self.month_combo.view().setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.month_combo.view().setMouseTracking(False)
        for d in range(1, 13):
            self.month_combo.addItem(str(d))

        scroller.setupScrolling(self.day_combo.view())
        self.day_combo.view().setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.day_combo.view().setMouseTracking(False)
        for d in range(1, 32):
            self.day_combo.addItem(str(d))

        scroller.setupScrolling(self.year_combo.view())
        self.year_combo.view().setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.year_combo.view().setMouseTracking(False)
        year = datetime.now().year
        for y in range(year, year + constants.maxExpirationYear + 1):
            self.year_combo.addItem(str(y))

    def updateCategories(self):
        self.category_combo.clear()

        for category in self.categories:
            self.category_combo.addItem(category['name'], category['id'])

        if self.pending_category:
            self.category_combo.addItem('* ' + self.pending_category, self.pendingCategoryText)
        self.category_combo.addItem('<New Category>', self.newCategoryText)

    @pyqtSlot(int)
    def on_category_combo_currentIndexChanged(self, index):
        # If the user data is equal to the new category text identifier, then this is the New Category option selected
        if self.category_combo.currentData() == self.newCategoryText:
            virtualKb = VirtualKeyboard(self)
            virtualKb.lineEdit.setMaxLength(constants.maxCategoryNameLength)

            # If the user successfully closes the keyboard, then add the category
            if virtualKb.exec() == QDialog.Accepted:
                categoryID = self.dbManager.AddCategory(virtualKb.text)

                # Query db for categories since a new one was added, update combobox since new category added
                self.categories = self.dbManager.GetCategories(True)
                self.updateCategories()

                # Find the index with the user data for the new categoryID, then set the currentIndex to that
                self.category_combo.setCurrentIndex(self.category_combo.findData(categoryID))
            else:
                # Set current index to be the added category
                self.category_combo.setCurrentIndex(self.category_combo.count() - 2)

    @pyqtSlot(str)
    def on_itemName_textBox_textChanged(self, string):
        # The current item name in the textbox changed, see if there is an item in the database with this name already
        item = self.dbManager.GetItemFromInventory(name=string)
        if item:
            # If so, this wont create a new item but instead will use the existing item. Set category to the existing
            # item category and set favorite's item checked to existing item. Then disable these controls since they
            # cannot be configured
            self.category_combo.setCurrentIndex(self.category_combo.findData(item['category']))
            self.category_combo.setEnabled(False)
            self.favorites_check.setChecked(item['favorites_index'] is not None)
            self.favorites_check.setEnabled(False)
        else:
            # Otherwise, if the item does not exist, enable these controls since they are configurable
            self.category_combo.setEnabled(True)
            self.favorites_check.setEnabled(True)

    @pyqtSlot(str)
    def itemName_updateSuggestions(self, str):
        if str:
            prefixMatch = str + '%'
            anyMatch = '%' + prefixMatch
            self.itemNameModel.filterArgs = (prefixMatch, prefixMatch, anyMatch, anyMatch)
            self.itemNameModel.hideItems = False
        else:
            self.itemNameModel.hideItems = True
        self.itemNameModel.select()

    def ResetToDefault(self):
        self.itemName_textBox.setText('')
        self.category_combo.setCurrentIndex(0)
        self.itemQty_combo.setCurrentIndex(0)
        self.pkgQty_combo.setCurrentIndex(0)
        self.month_combo.setCurrentIndex(0)
        self.day_combo.setCurrentIndex(0)
        self.year_combo.setCurrentIndex(0)
        self.favorites_check.setChecked(False)

    @pyqtSlot(bool, bool)
    def on_accept_button_clicked(self, checked, longPressed):
        if len(self.itemName_textBox.text()) > 0:
            self.accept()
        else:
            logger.warning("Invalid (empty) name entered into new item details dialog box.")

    @pyqtSlot(bool, bool)
    def on_cancel_button_clicked(self, checked, longPressed):
        self.close()
