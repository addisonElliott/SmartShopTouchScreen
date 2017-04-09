from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Windows.mainWindow import *
from Windows.favoriteWindow import *
from Windows.purchaseHistoryWindow import *
from Windows.settingsWindow import *
from Util.scanner import *
from Util.enums import *
from Util.databaseManager import *
from Util import constants
from datetime import *
import logging
import pickle
import os

from Widgets.touchSpinBox import *

logger = logging.getLogger(__name__)

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

        # Add purchase history window to list of stacked widgets
        self.purchaseHistoryWindow = PurchaseHistoryWindow(self, self.config, self.dbManager, self.stackedWidget)
        self.stackedWidget.addWidget(self.purchaseHistoryWindow)

        # Add settings window to list of stacked widgets
        self.settingsWindow = SettingsWindow(self, self.config, self.dbManager, self.stackedWidget)
        self.stackedWidget.addWidget(self.settingsWindow)

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

        # Create timer that will update the usage rates each day at constants.usageRateTime
        # Calls the updateUsageRates function within the timer callback. Also, call the updateUsageRates function initially
        # just to get caught up
        desiredDateTime = datetime.combine(datetime.now().date() + timedelta(days=1), constants.usageRateTime)
        timeUntilDate = desiredDateTime - datetime.now()

        self.usageRateUpdateTimer = QTimer()
        self.usageRateUpdateTimer.setTimerType(Qt.VeryCoarseTimer)
        self.usageRateUpdateTimer.setSingleShot(True)
        self.usageRateUpdateTimer.timeout.connect(self.usageRateUpdateTimer_ticked)
        self.usageRateUpdateTimer.start(timeUntilDate.total_seconds() * 1000.0)
        self.updateUsageRates()

    def updateUsageRates(self):
        if os.path.exists('usageRate.pickle'):
            with open('usageRate.pickle', 'rb') as f:
                lastUsageRateDateChecked = pickle.load(f)
        else:
            lastUsageRateDateChecked = None

        usageList = self.dbManager.getUsageHistory(lastUsageRateDateChecked)
        lastItem = -1
        prevDate = lastUsageRateDateChecked
        updateUsageRateDict = {}
        curDate = datetime.now().date()
        for usageItem in usageList:
            # Check if this item has a new item ID
            if lastItem != usageItem['item']:
                lastItem = usageItem['item']

                # If the avg_usage_rate is empty or the last usage check date is, set the initial avg_usage_rate to be
                # the first item (A.K.A oldest in the list). Otherwise, set the initial avg_usage_rate to be the old
                # avg_usage_rate divided by the number of days between now and the last time checked
                if usageItem['avg_usage_rate'] is None or lastUsageRateDateChecked is None:
                    daysDelta = (curDate - usageItem['date']).days
                    updateUsageRateDict[usageItem['item']] = usageItem['qty'] / 2**daysDelta
                else:
                    daysDelta = (curDate - lastUsageRateDateChecked).days
                    updateUsageRateDict[usageItem['item']] = usageItem['avg_usage_rate'] / 2**daysDelta

            # This is equal to (n - days) by taking the number of days.
            # The number of days between today and the usage date of the item
            # Increment the usage rate to be the quantity used on that day divided by 2^(# of days until today)
            daysDelta = (curDate - usageItem['date']).days
            updateUsageRateDict[usageItem['item']] += usageItem['qty'] / 2**(daysDelta)

        # Update the updateusageRateDict
        updateUsageRateList = updateUsageRateDict.items()
        updateUsageRateList = [(t[1], t[0]) for t in updateUsageRateList]
        self.dbManager.updateUsageRates(updateUsageRateList)
        logger.debug('Updating usage rates: %r' % updateUsageRateDict)

        # Save the last used
        with open('usageRate.pickle', 'wb') as f:
            pickle.dump(curDate, f)

    @pyqtSlot()
    def usageRateUpdateTimer_ticked(self):
        self.updateUsageRates()

        # Active timer again for tomorrow at the time usageRateTime in constants
        desiredDateTime = datetime.combine(datetime.now().date() + timedelta(days=1), constants.usageRateTime)
        timeUntilDate = desiredDateTime - datetime.now()

        logger.info('Calculating usage rate for all items in database. Set next update to be at %s',
                    str(desiredDateTime))
        self.usageRateUpdateTimer.start(timeUntilDate.total_seconds() * 1000.0)

        self.primaryScanner.barcodeReceived.connect(self.primaryScanner_barcodeReceived)
        self.secondaryScanner.barcodeReceived.connect(self.secondaryScanner_barcodeReceived)

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