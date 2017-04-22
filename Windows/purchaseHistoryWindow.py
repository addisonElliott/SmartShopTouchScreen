from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Windows.centralWindow import *
from Windows import purchaseHistoryWindow_ui
from Util import constants, scroller
from Util.enums import *
from Util.SqlTableModel import *
import logging

logger = logging.getLogger(__name__)

class PurchaseHistoryWindow(QWidget, purchaseHistoryWindow_ui.Ui_PurchaseHistoryWindow):
    def __init__(self, centralWindow, config, dbManager, parent=None):
        super(PurchaseHistoryWindow, self).__init__(parent)
        self.setupUi(self)

        self.centralWindow = centralWindow
        self.config = config
        self.dbManager = dbManager

        self.model = SqlTableModel(self.dbManager.connection, displayColumnMapping = (2, 0, 1),
                    displayHeaders=('Name', 'Purchase Date', 'Qty'),
                    customQuery = 'SELECT date, qty, '
                    '(SELECT name FROM inventory WHERE item = history.item) AS name FROM purchase_history history ')
        self.model.setColumnAlignment(1, Qt.AlignCenter)
        self.model.setColumnAlignment(2, Qt.AlignCenter)

        self.historyView.setModel(self.model)

        # Setup sorting on the model and list view (default is the date column descending)
        self.model.setSort('date', Qt.DescendingOrder)
        self.historyView.sortByColumn(1, Qt.DescendingOrder)

        # Set the name column to stretch to fill the area while the qty column is resized to contents
        self.historyView.horizontalHeader().setStretchLastSection(False)
        self.historyView.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.historyView.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.historyView.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        scroller.setupScrolling(self.historyView)

    @pyqtSlot()
    def showEvent(self, event):
        # Update the model in case any data has changed and reset sorting back by date
        self.model.select()
        self.historyView.sortByColumn(1, Qt.DescendingOrder)

    @pyqtSlot()
    def hideEvent(self, event):
        pass

    @pyqtSlot(bool, bool)
    def on_backBtn_clicked(self, checked, longPressed):
        self.parent().setCurrentIndex(WindowType.Main)

    @pyqtSlot(bool, bool)
    def on_homeBtn_clicked(self, checked, longPressed):
        self.parent().setCurrentIndex(WindowType.Main)
