from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Windows.centralWindow import *
from Windows import settingsWindow_ui
from Util import constants, scroller
from Util.enums import *
from Util.SqlTableModel import *
import logging

logger = logging.getLogger(__name__)

class SettingsWindow(QWidget, settingsWindow_ui.Ui_SettingsWindow):
    def __init__(self, centralWindow, config, dbManager, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.setupUi(self)

        self.centralWindow = centralWindow
        self.config = config
        self.dbManager = dbManager

    @pyqtSlot()
    def showEvent(self, event):
        self.centralWindow.primaryScanner.barcodeReceived.connect(self.primaryScanner_barcodeReceived)
        self.centralWindow.secondaryScanner.barcodeReceived.connect(self.secondaryScanner_barcodeReceived)

    @pyqtSlot()
    def hideEvent(self, event):
        self.centralWindow.primaryScanner.barcodeReceived.disconnect(self.primaryScanner_barcodeReceived)
        self.centralWindow.secondaryScanner.barcodeReceived.disconnect(self.secondaryScanner_barcodeReceived)

    @pyqtSlot(bool, bool)
    def on_backBtn_clicked(self, checked, longPressed):
        self.parent().setCurrentIndex(WindowType.Main)

    @pyqtSlot(bool, bool)
    def on_homeBtn_clicked(self, checked, longPressed):
        self.parent().setCurrentIndex(WindowType.Main)

    @pyqtSlot(str)
    def primaryScanner_barcodeReceived(self, barcode):
        logger.info("Primary barcode scanned in Settings's Menu: Note, this does nothing. You must be on the main menu")

    @pyqtSlot(str)
    def secondaryScanner_barcodeReceived(self, barcode):
        logger.info("Secondary barcode scanned in Settings's Menu: Note, this does nothing. You must be on the main menu")
