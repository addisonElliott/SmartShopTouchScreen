from Windows import ExpirationBox_ui
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Util import constants
from Util import scroller
from datetime import datetime

class ExpirationBox(QDialog, ExpirationBox_ui.Ui_ExpirationBox):
    def __init__(self, config, centralWindow, parent=None):
        super(ExpirationBox, self).__init__(parent)
        self.setupUi(self)

        self.config = config
        self.centralWindow = centralWindow

        # Remove title bar
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)

        scroller.setupScrolling(self.month_combo.view())
        # Set the combobox view to scroll per pixel so the kinetic scrolling via touchscreen isnt ridiculously fast
        self.month_combo.view().setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # Disabling mouse tracking means that when you first use touchscreen to scroll through items, then it wont
        # select that item
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

        scroller.setupScrolling(self.qty_combo.view())
        self.qty_combo.view().setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.qty_combo.view().setMouseTracking(False)
        for q in range(1, 51):
            self.qty_combo.addItem(str(q))

        # Setup timer to regularly poll for new barcodes from scanners
        self.scannerPoll = QTimer()
        self.scannerPoll.timeout.connect(self.scannerPoll_ticked)
        self.scannerPoll.start(constants.scannerPollInterval)

    @pyqtSlot()
    def scannerPoll_ticked(self):
        self.centralWindow.primaryScanner.poll()
        self.centralWindow.secondaryScanner.poll()

    @pyqtSlot(bool, bool)
    def on_accept_button_clicked(self, checked, longPressed):
        self.accept()

    @pyqtSlot(bool, bool)
    def on_cancel_button_clicked(self, checked, longPressed):
        self.close()
