from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Windows import mainWindow_ui
from Util import constants
from Windows.favoriteWindow import *
from Windows.centralWindow import *
from Util.scanner import *
from Util.enums import *


class MainWindow(QWidget, mainWindow_ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # Set size of the recommended items columns
        self.recItemsWidget.horizontalHeader().setStretchLastSection(False)
        self.recItemsWidget.horizontalHeader().setSectionResizeMode(1,QHeaderView.ResizeToContents)
        self.recItemsWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        # Setup primary and secondary scanner based on if the shortcuts should be enabled
        #if constants.barcodeScannerShortcut:
            #self.primaryScanner = BarcodeScanner(self, self.config['Scanners']['primaryPort'], "Ctrl+1", "primary")
            #self.secondaryScanner = BarcodeScanner(self, self.config['Scanners']['secondaryPort'], "Ctrl+2", "secondary")
        #else:
            #self.primaryScanner = BarcodeScanner(self, self.config['Scanners']['primaryPort'])
            #self.secondaryScanner = BarcodeScanner(self, self.config['Scanners']['secondaryPort'])

        #self.primaryScanner.barcodeReceived.connect(self.primaryScanner_barcodeReceived)
        #self.secondaryScanner.barcodeReceived.connect(self.secondaryScanner_barcodeReceived)

        # Setup timer to regularly poll for new barcodes from scanners
        #self.parent().scannerPoll.timeout.connect(self.scannerPoll_ticked)

        #self.scannerPoll = QTimer()
        #self.scannerPoll.timeout.connect(self.scannerPoll_ticked)
        #self.scannerPoll.start(constants.scannerPollInterval)

    @pyqtSlot()
    def showEvent(self, event):
        print('Yes baby')

    @pyqtSlot()
    def hideEvent(self, event):
        print('Aww...');

    @pyqtSlot()
    def on_purchaseHistoryBtn_clicked(self):
        self.close()

    @pyqtSlot()
    def on_ManualAddButton_clicked(self):
        self.parent().setCurrentIndex(WindowType.Favorites)

    @pyqtSlot()
    def on_SettingsButton_clicked(self):
        self.centralWindow.close()

    @pyqtSlot()
    def scannerPoll_ticked(self):
        self.primaryScanner.poll()
        self.secondaryScanner.poll()

    @pyqtSlot(str)
    def primaryScanner_barcodeReceived(self, barcode):
        print("Primary barcode scanner got: %s" % barcode)
        # TODO Send the barcode scanner information to be processed
        
    @pyqtSlot(str)
    def secondaryScanner_barcodeReceived(self, barcode):
        print("Secondary barcode scanner got: %s" % barcode)
        # TODO Send the barcode scanner information to be processed