from Windows import NewItemDetails_ui
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Util import constants
from Util import scroller
from datetime import datetime


class NewItemDetails(QDialog, NewItemDetails_ui.Ui_NewItemDetails):
    def __init__(self, config, categories, parent=None):
        super(NewItemDetails, self).__init__(parent)
        self.setupUi(self)

        self.config = config

        # Remove title bar
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)

        scroller.setupScrolling(self.category_combo.view())
        # Set the combobox view to scroll per pixel so the kinetic scrolling via touchscreen isnt ridiculously fast
        self.category_combo.view().setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # Disabling mouse tracking means that when you first use touchscreen to scroll through items, then it wont
        # select that item
        self.category_combo.view().setMouseTracking(False)
        for category in categories:
            self.category_combo.addItem(category['name'])

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

    @pyqtSlot(bool, bool)
    def on_accept_button_clicked(self, checked, longPressed):
        self.accept()

    @pyqtSlot(bool, bool)
    def on_cancel_button_clicked(self, checked, longPressed):
        self.close()
