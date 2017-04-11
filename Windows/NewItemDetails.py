from Windows import NewItemDetails_ui
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Util import constants
from Util import scroller
from datetime import datetime


class NewItemDetails(QDialog, NewItemDetails_ui.Ui_NewItemDetails):
    def __init__(self, config, parent=None):
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
        #self.month_combo.setCurrentIndex(datetime.now().month - 1)
        for d in range(1, 32):
            self.day_combo.addItem(str(d))
        #self.day_combo.setCurrentIndex(datetime.now().day - 1)
        year = datetime.now().year
        for y in range(year, year + constants.maxExpirationYear + 1):
            self.year_combo.addItem(str(y))
        for q in range(1, 51):
            self.pkgQty_combo.addItem(str(q))
        for q in range(1, 51):
            self.itemQty_combo.addItem(str(q))

    @pyqtSlot(bool, bool)
    def on_accept_button_clicked(self, checked, longPressed):
        self.accept()

    @pyqtSlot(bool, bool)
    def on_cancel_button_clicked(self, checked, longPressed):
        self.close()
