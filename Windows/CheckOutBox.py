from Windows import CheckOutBox_ui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Util import scroller
from Util import constants

class CheckOutBox(QDialog, CheckOutBox_ui.Ui_CheckOutBox):
    def __init__(self, config, centralWindow, parent=None):
        super(CheckOutBox, self).__init__(parent)
        self.setupUi(self)

        self.config = config
        self.centralWindow = centralWindow

        # Remove title bar
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)

        scroller.setupScrolling(self.qty_combo.view())
        self.qty_combo.view().setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.qty_combo.view().setMouseTracking(False)
        for q in range(1, 51):
            self.qty_combo.addItem(str(q))

        self.callbackFunction = None
        self.callbackParam = None

    @pyqtSlot()
    def showEvent(self, event):
        # Setup timer to regularly poll for new barcodes from scanners
        self.scannerPoll = QTimer()
        self.scannerPoll.timeout.connect(self.scannerPoll_ticked)
        self.scannerPoll.start(constants.scannerPollInterval)

        # Disconnect the function within centralWindow to handle barcode scanning and setup our own custom functions
        self.centralWindow.primaryScanner.barcodeReceived.connect(self.primaryScanner_barcodeReceived)
        self.centralWindow.secondaryScanner.barcodeReceived.connect(self.secondaryScanner_barcodeReceived)
        self.centralWindow.primaryScanner.barcodeReceived.disconnect(self.centralWindow.primaryScanner_barcodeReceived)
        self.centralWindow.secondaryScanner.barcodeReceived.disconnect(self.centralWindow.secondaryScanner_barcodeReceived)

    @pyqtSlot()
    def hideEvent(self, event):
        # Reconnect the function within centralWindow to handle barcode scanning and disconnect our custom functions
        self.centralWindow.primaryScanner.barcodeReceived.disconnect(self.primaryScanner_barcodeReceived)
        self.centralWindow.secondaryScanner.barcodeReceived.disconnect(self.secondaryScanner_barcodeReceived)
        self.centralWindow.primaryScanner.barcodeReceived.connect(self.centralWindow.primaryScanner_barcodeReceived)
        self.centralWindow.secondaryScanner.barcodeReceived.connect(self.centralWindow.secondaryScanner_barcodeReceived)

    @pyqtSlot()
    def scannerPoll_ticked(self):
        self.centralWindow.primaryScanner.poll()
        self.centralWindow.secondaryScanner.poll()

    @pyqtSlot(str)
    def primaryScanner_barcodeReceived(self, barcode):
        self.callbackFunction = self.centralWindow.primaryScanner_barcodeReceived
        self.callbackParam = barcode

        # Close this dialog box, indicate to parent what the callback function and parameter should be
        self.accept()

    @pyqtSlot(str)
    def secondaryScanner_barcodeReceived(self, barcode):
        self.callbackFunction = self.centralWindow.secondaryScanner_barcodeReceived
        self.callbackParam = barcode

        # Close this dialog box, indicate to parent what the callback function and parameter should be
        self.accept()

    @pyqtSlot(bool, bool)
    def on_accept_button_clicked(self, checked, longPressed):
        self.accept()

    @pyqtSlot(bool, bool)
    def on_cancel_button_clicked(self, checked, longPressed):
        self.close()
