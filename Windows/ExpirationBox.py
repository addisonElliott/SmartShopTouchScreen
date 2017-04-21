from Windows import ExpirationBox_ui
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Util import constants
from Util import scroller
from datetime import datetime

class ExpirationBox(QDialog, ExpirationBox_ui.Ui_ExpirationBox):
    def __init__(self, config, parent=None):
        super(ExpirationBox, self).__init__(parent)
        self.setupUi(self)

        self.config = config

        # Remove title bar
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)

        scroller.setupScrolling(self.month_combo.view())
        scroller.setupScrolling(self.day_combo.view())
        scroller.setupScrolling(self.year_combo.view())
        scroller.setupScrolling(self.qty_combo.view())

        for d in range(1, 13):
            self.month_combo.addItem(str(d))
        for d in range(1, 32):
            self.day_combo.addItem(str(d))
        year = datetime.now().year
        for y in range(year, year + constants.maxExpirationYear + 1):
            self.year_combo.addItem(str(y))
        for q in range(1, 51):
            self.qty_combo.addItem(str(q))

        self.raise_()

    @pyqtSlot(bool, bool)
    def on_accept_button_clicked(self, checked, longPressed):
        self.accept()

    @pyqtSlot(bool, bool)
    def on_cancel_button_clicked(self, checked, longPressed):
        self.close()
