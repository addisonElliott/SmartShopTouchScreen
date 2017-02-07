import mainWindow_ui
from scanner import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import constants

class MainWindow(QMainWindow, mainWindow_ui.Ui_MainWindow):
    def __init__(self, config, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.config = config

        # Remove title bar to
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Sets position to 0,0 on screen and sets window to fixed size
        self.setGeometry(QRect(0, 0, 800, 480))

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
        # TODO Consider having a constants file where I can set the interval for the scannerPoll timer. This doesnt need
        # to be a setting however
        self.scannerPoll = QTimer()
        self.scannerPoll.timeout.connect(self.scannerPoll_ticked)
        self.scannerPoll.start(5)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.close()

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