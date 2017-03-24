from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import mainWindow_ui
from Util import constants
from favoriteWindow import *
from scanner import *


class MainWindow(QMainWindow, mainWindow_ui.Ui_MainWindow):
    def __init__(self, config, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.config = config
        self.recItemsWidget.horizontalHeader().setStretchLastSection(False)
        self.recItemsWidget.horizontalHeader().setSectionResizeMode(1,QHeaderView.ResizeToContents)
        self.recItemsWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)


        # Remove title bar
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Sets position to 0,0 on screen and sets window to fixed size
        self.setGeometry(constants.windowGeometry)

        # Set size of the recommended items columns

        # Create shortcut for escape key that calls close()
        self.closeShortcut = QShortcut(Qt.Key_Escape, self)
        self.closeShortcut.activated.connect(self.close)

        # Setup primary and secondary scanner based on if the shortcuts should be enabled
        if constants.barcodeScannerShortcut:
            self.primaryScanner = BarcodeScanner(self, self.config['Scanners']['primaryPort'], "Ctrl+1", "primary")
            self.secondaryScanner = BarcodeScanner(self, self.config['Scanners']['secondaryPort'], "Ctrl+2", "secondary")
        else:
            self.primaryScanner = BarcodeScanner(self, self.config['Scanners']['primaryPort'])
            self.secondaryScanner = BarcodeScanner(self, self.config['Scanners']['secondaryPort'])

        self.primaryScanner.barcodeReceived.connect(self.primaryScanner_barcodeReceived)
        self.secondaryScanner.barcodeReceived.connect(self.secondaryScanner_barcodeReceived)

        # Setup timer to regularly poll for new barcodes from scanners
        self.scannerPoll = QTimer()
        self.scannerPoll.timeout.connect(self.scannerPoll_ticked)
        self.scannerPoll.start(constants.scannerPollInterval)

    @pyqtSlot()
    def on_purchaseHistoryBtn_clicked(self):
        self.close()

    @pyqtSlot()
    def on_ManualAddButton_clicked(self):
        ManualAdd = ManualAddDialog(self.config)
        ManualAdd.exec()

    @pyqtSlot()
    def on_SettingsButton_clicked(self):
        self.fav = FavoriteWindow(self.config)
        if constants.fullscreen:
            self.fav.showFullScreen()
        else:
            self.fav.show()
        #self.close()

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