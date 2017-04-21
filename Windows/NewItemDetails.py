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
        self.setWindowFlags(Qt.FramelessWindowHint)

        scroller.setupScrolling(self.category_combo.view())
        scroller.setupScrolling(self.itemQty_combo.view())
        scroller.setupScrolling(self.pkgQty_combo.view())
        scroller.setupScrolling(self.month_combo.view())
        scroller.setupScrolling(self.day_combo.view())
        scroller.setupScrolling(self.year_combo.view())

        for d in range(1, 13):
            self.month_combo.addItem(str(d))
        for d in range(1, 32):
            self.day_combo.addItem(str(d))
        year = datetime.now().year
        for y in range(year, year + constants.maxExpirationYear + 1):
            self.year_combo.addItem(str(y))
        for q in range(1, 51):
            self.pkgQty_combo.addItem(str(q))
        for q in range(1, 51):
            self.itemQty_combo.addItem(str(q))
        for category in categories:
            self.category_combo.addItem(category['name'])

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
        self.accept()

    @pyqtSlot(bool, bool)
    def on_cancel_button_clicked(self, checked, longPressed):
        self.close()
