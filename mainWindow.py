import mainWindow_ui
from scanner import BarcodeScanner
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtCore import *

class MainWindow(QMainWindow, mainWindow_ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # TODO Load settings here. This will load the previously saved settings

        # Remove title bar to
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Sets position to 0,0 on screen and sets window to fixed size
        self.setGeometry(0, 0, 800, 480)

        # TODO The primary and secondary scanner should be defined based on prev
        # settings
        self.primaryScanner = BarcodeScanner(4);
        self.primaryScanner.barcodeReceived.connect(self.primaryScanner_barcodeReceived)
        self.secondaryScanner = BarcodeScanner(5);
        self.secondaryScanner.barcodeReceived.connect(self.secondaryScanner_barcodeReceived)

        # Setup timer to regularly poll for new barcodes from scanners
        # TODO Consider having a constants file where I can set the interval for
        # the scannerPoll timer. This doesnt need to be a setting however
        self.scannerPoll = QTimer()
        self.scannerPoll.timeout.connect(self.scannerPoll_ticked)
        self.scannerPoll.start(2)

    @pyqtSlot()
    def keyPressEvent(self, event):
        # Pressing escape will kill the application since the title bar is absent
        if event.key() == Qt.Key_Escape:
            self.close()

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
        
    @pyqtSlot(str)
    def secondaryScanner_barcodeReceived(self, barcode):
        print("Secondary barcode scanner got: %s" % barcode)
