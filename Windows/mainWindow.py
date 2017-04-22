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

        self.reqItemsWidget.setModel(self.reqItemsModel)
        self.recItemsWidget.setModel(self.recItemsModel)
        self.reqItemsWidget.selectionModel().selectionChanged.connect(self.selectItem)
        self.recItemsWidget.selectionModel().selectionChanged.connect(self.selectItem)

        # Configure floating buttons
        self.gridLayout_3.removeWidget(self.floatingPB1)
        self.floatingPB1.hide()
        self.floatingPB1.setEnabled(False)
        self.floatingPB1.setGeometry(constants.removeReqShoppingItemBtnGeometry)
        self.floatingPB1.raise_()

        self.gridLayout_3.removeWidget(self.floatingPB2)
        self.floatingPB2.hide()
        self.floatingPB2.setEnabled(False)
        self.floatingPB2.setGeometry(constants.removeRecShoppingItemBtnGeometry)
        self.floatingPB2.raise_()

    @pyqtSlot()
    def showEvent(self, event):
        # Update the two shopping lists in case any changes were made on a different menu
        self.reqItemsModel.select()
        self.recItemsModel.select()

        # Reset the sorting for each of the shopping lists
        self.reqItemsWidget.sortByColumn(0, Qt.AscendingOrder)
        self.recItemsWidget.sortByColumn(0, Qt.AscendingOrder)

        # Set size of the recommended items columns
        # Do this on showEvent because additional data could be added to the quantity column and require the contents
        # to be resized
        self.reqItemsWidget.horizontalHeader().setStretchLastSection(False)
        self.reqItemsWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.reqItemsWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.recItemsWidget.horizontalHeader().setStretchLastSection(False)
        self.recItemsWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.recItemsWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

    @pyqtSlot()
    def hideEvent(self, event):
        pass

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
    def selectItem(self):
        hasSelection = self.sender().hasSelection()
        if self.sender() is self.reqItemsWidget.selectionModel():
            self.floatingPB1.setEnabled(hasSelection)
            self.floatingPB1.setVisible(hasSelection)
        else:
            self.floatingPB2.setEnabled(hasSelection)
            self.floatingPB2.setVisible(hasSelection)
