from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Windows.mainWindow import *
from Windows.favoriteWindow import *
from Windows.purchaseHistoryWindow import *
from Util.scanner import *
from Util.enums import *
from Util.databaseManager import *
from Util import constants

from Widgets.touchSpinBox import *

class CentralWindow(QMainWindow):
    def __init__(self, config, parent=None):
        super(CentralWindow, self).__init__(parent)

        # Save config variable in class
        self.config = config

        self.dbManager = DatabaseManager(constants.dbDatabase, constants.dbUsername, constants.dbPassword,
                                    constants.dbHost, constants.dbPort)

        # Initialize central widget, horizontal layout and stacked which which fills the entire QMainWindow
        self.centralwidget = QWidget(self)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.horizontalLayout.addWidget(self.stackedWidget)
        self.setCentralWidget(self.centralwidget)

        # Add main window to list of stacked widgets
        self.mainWindow = MainWindow(self, self.config, self.dbManager, self.stackedWidget)
        self.stackedWidget.addWidget(self.mainWindow)

        # Add favorite window to list of stacked widgets
        self.favoriteWindow = FavoriteWindow(self, self.config, self.dbManager, self.stackedWidget)
        self.stackedWidget.addWidget(self.favoriteWindow)

        # Add favorite window to list of stacked widgets
        self.purchaseHistoryWindow = PurchaseHistoryWindow(self, self.config, self.dbManager, self.stackedWidget)
        self.stackedWidget.addWidget(self.purchaseHistoryWindow)

        # Set the current widget to be shown is the main
        self.stackedWidget.setCurrentIndex(WindowType.Main)

        # Remove title bar
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Sets position to 0,0 on screen and sets window to fixed size
        self.setGeometry(constants.windowGeometry)

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

        # Setup timer to regularly poll for new barcodes from scanners
        self.scannerPoll = QTimer()
        self.scannerPoll.timeout.connect(self.scannerPoll_ticked)
        self.scannerPoll.start(constants.scannerPollInterval)

        print(self.geometry())

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