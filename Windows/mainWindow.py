from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Windows import mainWindow_ui
from Util import constants
from Windows.NewItemDetails import NewItemDetails
from Windows.favoriteWindow import *
from Windows.centralWindow import *
from Util.scanner import *
from Util.enums import *
from BarcodeAPI.barcodeManager import BarcodeManager
from Util.SqlTableModel import *

class MainWindow(QWidget, mainWindow_ui.Ui_MainWindow):
    def __init__(self, centralWindow, config, dbManager, barcodeManager, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.centralWindow = centralWindow
        self.config = config
        self.dbManager = dbManager
        self.barcodeManager = barcodeManager

        self.reqItemsModel = SqlTableModel(self.dbManager.connection, 'inventory', 'name', Qt.AscendingOrder,
                                         'list_flags = 1',None, ('item', 'name', 'qty'), (1, 2), ('Name', 'Qty'))
        self.recItemsModel = SqlTableModel(self.dbManager.connection, 'inventory', 'name', Qt.AscendingOrder,
                                           'list_flags = 2', None, ('item', 'name', 'qty'), (1, 2), ('Name', 'Qty'))

        self.reqItemsTableView.setModel(self.reqItemsModel)
        self.recItemsTableView.setModel(self.recItemsModel)
        self.reqItemsTableView.selectionModel().selectionChanged.connect(self.selectItem)
        self.recItemsTableView.selectionModel().selectionChanged.connect(self.selectItem)

        # Configure floating buttons
        self.gridLayout_3.removeWidget(self.reqItemsRemoveBtn)
        self.reqItemsRemoveBtn.hide()
        self.reqItemsRemoveBtn.setEnabled(False)
        self.reqItemsRemoveBtn.setGeometry(constants.removeReqShoppingItemBtnGeometry)
        self.reqItemsRemoveBtn.raise_()

        self.gridLayout_3.removeWidget(self.recItemsRemoveBtn)
        self.recItemsRemoveBtn.hide()
        self.recItemsRemoveBtn.setEnabled(False)
        self.recItemsRemoveBtn.setGeometry(constants.removeRecShoppingItemBtnGeometry)
        self.recItemsRemoveBtn.raise_()

    @pyqtSlot()
    def showEvent(self, event):
        # Update the two shopping lists in case any changes were made on a different menu
        self.reqItemsModel.select()
        self.recItemsModel.select()

        # Reset the sorting for each of the shopping lists
        self.reqItemsTableView.sortByColumn(0, Qt.AscendingOrder)
        self.recItemsTableView.sortByColumn(0, Qt.AscendingOrder)

        # Set size of the recommended items columns
        # Do this on showEvent because additional data could be added to the quantity column and require the contents
        # to be resized
        self.reqItemsTableView.horizontalHeader().setStretchLastSection(False)
        self.reqItemsTableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.reqItemsTableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.recItemsTableView.horizontalHeader().setStretchLastSection(False)
        self.recItemsTableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.recItemsTableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.centralWindow.updateRecommendedItemsTimer.timeout.connect(self.updateRecommendedItemsTimer_ticked)

    @pyqtSlot()
    def hideEvent(self, event):
        self.centralWindow.updateRecommendedItemsTimer.timeout.disconnect(self.updateRecommendedItemsTimer_ticked)

    @pyqtSlot(bool, bool)
    def on_ManualAddButton_clicked(self, checked, longPressed):
        self.parent().setCurrentIndex(WindowType.Favorites)

    @pyqtSlot(bool, bool)
    def on_PurchaseHistoryButton_clicked(self, checked, longPressed):
        self.parent().setCurrentIndex(WindowType.PurchaseHistory)

    @pyqtSlot(bool, bool)
    def on_SettingsButton_clicked(self, checked, longPressed):
        self.parent().setCurrentIndex(WindowType.Settings)

    @pyqtSlot()
    def updateRecommendedItemsTimer_ticked(self):
        # When the recommended items are updated, refresh the database to show any changes
        self.recItemsModel.select()

    @pyqtSlot(bool, bool)
    def on_reqItemsRemoveBtn_clicked(self, checked, longPressed):
        records = self.reqItemsModel.getSelectedRecords(self.reqItemsTableView.selectionModel().selectedRows())

        for record in records:
            self.dbManager.removeItemFromRequiredList(record['item'])

        self.reqItemsModel.select()
        self.reqItemsRemoveBtn.setEnabled(False)
        self.reqItemsRemoveBtn.setVisible(False)

    @pyqtSlot(bool, bool)
    def on_recItemsRemoveBtn_clicked(self, checked, longPressed):
        records = self.recItemsModel.getSelectedRecords(self.recItemsTableView.selectionModel().selectedRows())

        for record in records:
            self.dbManager.removeItemFromRecommendedList(record['item'])

        self.recItemsModel.select()
        self.recItemsRemoveBtn.setEnabled(False)
        self.recItemsRemoveBtn.setVisible(False)

    @pyqtSlot()
    def selectItem(self):
        hasSelection = self.sender().hasSelection()
        if self.sender() is self.reqItemsTableView.selectionModel():
            self.reqItemsRemoveBtn.setEnabled(hasSelection)
            self.reqItemsRemoveBtn.setVisible(hasSelection)
        else:
            self.recItemsRemoveBtn.setEnabled(hasSelection)
            self.recItemsRemoveBtn.setVisible(hasSelection)
