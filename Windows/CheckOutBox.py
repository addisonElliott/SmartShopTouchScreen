from Windows import CheckOutBox_ui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Util import scroller

class CheckOutBox(QDialog, CheckOutBox_ui.Ui_CheckOutBox):
    def __init__(self, config, parent=None):
        super(CheckOutBox, self).__init__(parent)
        self.setupUi(self)

        self.config = config
        # Remove title bar
        self.setWindowFlags(Qt.FramelessWindowHint)

        scroller.setupScrolling(self.qty_combo.view())

        for q in range(1, 51):
            self.qty_combo.addItem(str(q))

    @pyqtSlot(bool, bool)
    def on_accept_button_clicked(self, checked, longPressed):
        self.accept()

    @pyqtSlot(bool, bool)
    def on_cancel_button_clicked(self, checked, longPressed):
        self.close()
