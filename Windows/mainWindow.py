from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Windows import mainWindow_ui
from Util import constants
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

        # Temporary to test Auto-Complete Virtual Keyboard
        self.tempShortcut = QShortcut(Qt.Key_1, self)
        self.tempShortcut.activated.connect(self.temp)

        # Set size of the recommended items columns
        self.recItemsWidget.horizontalHeader().setStretchLastSection(False)
        self.recItemsWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.recItemsWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.barcodeManager = barcodeManager

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
        pass

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

    @pyqtSlot()
    def scannerPoll_ticked(self):
        self.primaryScanner.poll()
        self.secondaryScanner.poll()
