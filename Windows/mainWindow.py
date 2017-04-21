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



from Windows.virtualKeyboard import *
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

        # Temporary to test Auto-Complete Virtual Keyboard
        self.tempShortcut = QShortcut(Qt.Key_1, self)
        self.tempShortcut.activated.connect(self.temp)

        # Configure floating buttons
        self.gridLayout_3.removeWidget(self.floatingPB1)
        self.floatingPB1.hide()
        self.floatingPB1.setEnabled(False)
        floatingPB1Width = 70
        floatingPB1Height = 70
        floatingPB1X = 280
        floatingPB1Y = 390
        self.floatingPB1.setGeometry(floatingPB1X, floatingPB1Y, floatingPB1Width, floatingPB1Height)
        self.floatingPB1.raise_()

        self.gridLayout_3.removeWidget(self.floatingPB2)
        self.floatingPB2.setEnabled(False)
        self.floatingPB2.hide()
        floatingPB2Width = 70
        floatingPB2Height = 70
        floatingPB2X = 630
        floatingPB2Y = 390
        self.floatingPB2.setGeometry(floatingPB2X, floatingPB2Y, floatingPB2Width, floatingPB2Height)
        self.floatingPB2.raise_()

    def temp2(self, str):
        if str:
            prefixMatch = str + '%'
            anyMatch = '%' + prefixMatch
            self.testModel.filterArgs = (prefixMatch, prefixMatch, anyMatch, anyMatch)
            self.testModel.hideItems = False
        else:
            self.testModel.hideItems = True
        self.testModel.select()

    @pyqtSlot()
    def temp(self):
        # TODO Remove this function and the one above temp2 when auto complete virtual keyboard is integrated correctly
        # TODO Also DONT FORGET TO REMOVE VIRTUAL KEYBOARD IMPORT
        self.testModel = SqlTableModel(self.dbManager.connection, columnSortName='rank', columnSortOrder=Qt.DescendingOrder,
                                       customQuery='SELECT item, name, CASE\n'
                                        'WHEN name LIKE %s THEN 3\n'
                                        'WHEN name ILIKE %s THEN 2\n'
                                        'WHEN name LIKE %s THEN 1\n'
                                        'ELSE 0 END AS rank FROM inventory\n'
                                        'WHERE name ILIKE %s', filterArgs=('%', '%%', '%', '%%'),
                                       displayColumnMapping=(1,), limitCount = 10, hideItems=True)

        self.test = VirtualKeyboard(self, None, self.testModel)
        self.test.updateSuggestions.connect(self.temp2)
        self.test.exec()

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
    def on_checkInOutBtn_clicked(self, checked, longPressed):
        print('Button hit: checked: %r longPress: %r' % (checked, longPressed))
        print('yesss')

    @pyqtSlot(bool, bool)
    def on_ManualAddButton_clicked(self, checked, longPressed):
        self.parent().setCurrentIndex(WindowType.Favorites)

    @pyqtSlot(bool, bool)
    def on_PurchaseHistoryButton_clicked(self, checked, longPressed):
        self.parent().setCurrentIndex(WindowType.PurchaseHistory)

    @pyqtSlot(bool, bool)
    def on_SettingsButton_clicked(self, checked, longPressed):
        self.parent().setCurrentIndex(WindowType.Settings)

    @pyqtSlot(bool, bool)
    def on_checkInOutBtn_clicked(self, checked, longPressed):
        print('Button hit: checked: %r longPress: %r' % (checked, longPressed))
        print('yesss')

    @pyqtSlot()
    def scannerPoll_ticked(self):
        self.primaryScanner.poll()
        self.secondaryScanner.poll()

    @pyqtSlot(str)
    def primaryScanner_barcodeReceived(self, barcode):
        print("Main: Primary barcode scanner got: %s" % barcode)
        # TODO Send the barcode scanner information to be processed

    @pyqtSlot(str)
    def secondaryScanner_barcodeReceived(self, barcode):
        print("Main: Secondary barcode scanner got: %s" % barcode)
        # TODO Send the barcode scanner information to be processed.

    @pyqtSlot()
    def selectItem(self):
        hasSelection = self.sender().hasSelection()
        print('has selection %r' % (hasSelection))
        if self.sender() is self.reqItemsWidget.selectionModel():
            self.floatingPB1.setEnabled(hasSelection)
            self.floatingPB1.setVisible(hasSelection)
        else:
            self.floatingPB2.setEnabled(hasSelection)
            self.floatingPB2.setVisible(hasSelection)
