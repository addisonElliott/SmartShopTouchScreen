from Windows import NewItemDetails_ui
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Util import constants
from Util import scroller
from datetime import datetime
from Windows.virtualKeyboard import *


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

    @pyqtSlot(bool, bool)
    def on_accept_button_clicked(self, checked, longPressed):
        self.accept()

    @pyqtSlot(bool, bool)
    def on_cancel_button_clicked(self, checked, longPressed):
        self.close()
