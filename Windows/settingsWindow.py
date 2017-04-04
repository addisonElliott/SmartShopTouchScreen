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

        # Set current index to first page
        self.settingsStack.setCurrentIndex(0)

    @pyqtSlot()
    def showEvent(self, event):
        self.centralWindow.primaryScanner.barcodeReceived.connect(self.primaryScanner_barcodeReceived)
        self.centralWindow.secondaryScanner.barcodeReceived.connect(self.secondaryScanner_barcodeReceived)

        # Move selected row to -1 so that no items are selected by default
        self.settingsView.setCurrentRow(-1)

        # Load the settings
        self.loadSettings()

    @pyqtSlot()
    def hideEvent(self, event):
        self.centralWindow.primaryScanner.barcodeReceived.disconnect(self.primaryScanner_barcodeReceived)
        self.centralWindow.secondaryScanner.barcodeReceived.disconnect(self.secondaryScanner_barcodeReceived)

        # Save the settings
        self.saveSettings()

    @pyqtSlot(bool, bool)
    def on_backBtn_clicked(self, checked, longPressed):
        if self.settingsStack.currentIndex() != 0:
            self.settingsStack.setCurrentIndex(0)
            self.settingsView.setCurrentRow(-1)
        else:
            self.parent().setCurrentIndex(WindowType.Main)

    @pyqtSlot(bool, bool)
    def on_homeBtn_clicked(self, checked, longPressed):
        self.parent().setCurrentIndex(WindowType.Main)

    @pyqtSlot(QListWidgetItem, QListWidgetItem)
    def on_settingsView_currentItemChanged(self, curItem, prevItem):
        self.settingsStack.setCurrentIndex(self.settingsView.indexFromItem(curItem).row() + 1)

    @pyqtSlot(bool, bool)
    def on_swapScannersBtn_clicked(self, checked, longPressed):
        temp = self.primaryLabel.text()
        self.primaryLabel.setText(self.secondaryLabel.text())
        self.secondaryLabel.setText(temp)

    @pyqtSlot(bool, bool)
    def on_shelfTimeCheckBox_clicked(self, checked, longPressed):
        self.shelfTimeSpinBox.setEnabled(checked)

    @pyqtSlot(bool, bool)
    def on_usageRateCheckBox_clicked(self, checked, longPressed):
        self.usageRateSpinBox.setEnabled(checked)

    @pyqtSlot(bool, bool)
    def on_expDateCheckBox_clicked(self, checked, longPressed):
        self.expDateSpinBox.setEnabled(checked)

    @pyqtSlot(str)
    def primaryScanner_barcodeReceived(self, barcode):
        logger.info("Primary barcode scanned in Settings's Menu: Note, this does nothing. You must be on the main menu")

    @pyqtSlot(str)
    def secondaryScanner_barcodeReceived(self, barcode):
        logger.info("Secondary barcode scanned in Settings's Menu: Note, this does nothing. You must be on the main menu")

    def loadSettings(self):
        # System Settings
        self.primaryLabel.setText(str(self.config['Scanners']['primaryPort']))
        self.secondaryLabel.setText(str(self.config['Scanners']['secondaryPort']))

        # Algorithm Settings
        self.shelfTimeCheckBox.setChecked(self.config['Algorithm']['enableShelfTime'])
        self.shelfTimeSpinBox.setValue(self.config['Algorithm']['shelfTimeThreshold'])
        self.shelfTimeSpinBox.setEnabled(self.shelfTimeCheckBox.isChecked())

        self.usageRateCheckBox.setChecked(self.config['Algorithm']['enableUsageRate'])
        self.usageRateSpinBox.setValue(self.config['Algorithm']['usageRateThreshold'])
        self.usageRateSpinBox.setEnabled(self.usageRateCheckBox.isChecked())

        self.expDateCheckBox.setChecked(self.config['Algorithm']['enableExpDate'])
        self.expDateSpinBox.setValue(self.config['Algorithm']['expDateThreshold'])
        self.expDateSpinBox.setEnabled(self.expDateCheckBox.isChecked())

    def saveSettings(self):
        # System Settings
        self.config['Scanners']['primaryPort'] = int(self.primaryLabel.text())
        self.config['Scanners']['secondaryPort'] = int(self.secondaryLabel.text())
        self.centralWindow.primaryScanner.setPort(self.config['Scanners']['primaryPort'])
        self.centralWindow.secondaryScanner.setPort(self.config['Scanners']['secondaryPort'])

        # Algorithm Settings
        self.config['Algorithm']['enableShelfTime'] = bool(self.shelfTimeCheckBox.isChecked())
        self.config['Algorithm']['shelfTimeThreshold'] = int(self.shelfTimeSpinBox.value())

        self.config['Algorithm']['enableUsageRate'] = bool(self.usageRateCheckBox.isChecked())
        self.config['Algorithm']['usageRateThreshold'] = int(self.usageRateSpinBox.value())

        self.config['Algorithm']['enableExpDate'] = bool(self.expDateCheckBox.isChecked())
        self.config['Algorithm']['expDateThreshold'] = int(self.expDateSpinBox.value())
