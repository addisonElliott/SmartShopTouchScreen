
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Windows import mainWindow_ui
from Util import constants
from Windows.favoriteWindow import *
from Windows.centralWindow import *
from Windows.ExpirationBox import *
from Util.scanner import *
from Util.enums import *

class MainWindow(QWidget, mainWindow_ui.Ui_MainWindow):
    def __init__(self, centralWindow, config, dbManager, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.centralWindow = centralWindow
        self.config = config
        self.dbManager = dbManager

        # Set size of the recommended items columns
        self.recItemsWidget.horizontalHeader().setStretchLastSection(False)
        self.recItemsWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.recItemsWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        #Configure floating buttons

        self.gridLayout_3.removeWidget(self.floatingPB1)
        self.floatingPB1.hide()
        self.floatingPB1.setEnabled(False)
        floatingPB1Width = 70#48 * 2 + 40
        floatingPB1Height = 70#48 + 12
        floatingPB1X = 280#(self.width() - floatingPB1Width) / 2
        floatingPB1Y = 390# self.height() - floatingPB1Height - 1
        self.floatingPB1.setGeometry(floatingPB1X, floatingPB1Y, floatingPB1Width, floatingPB1Height)
        self.floatingPB1.raise_()


        self.gridLayout_3.removeWidget(self.floatingPB2)
        self.floatingPB2.setEnabled(False)
        self.floatingPB2.hide()
        floatingPB2Width = 70  # 48 * 2 + 40
        floatingPB2Height = 70  # 48 + 12
        floatingPB2X = 630  # (self.width() - floatingPB1Width) / 2
        floatingPB2Y = 390  # self.height() - floatingPB1Height - 1
        self.floatingPB2.setGeometry(floatingPB2X, floatingPB2Y, floatingPB2Width, floatingPB2Height)
        self.floatingPB2.raise_()

    @pyqtSlot()
    def showEvent(self, event):
        self.centralWindow.primaryScanner.barcodeReceived.connect(self.primaryScanner_barcodeReceived)
        self.centralWindow.secondaryScanner.barcodeReceived.connect(self.secondaryScanner_barcodeReceived)
        print('This widget is being shown. Handle anything necessary. Main Window')

    @pyqtSlot()
    def hideEvent(self, event):
        self.centralWindow.primaryScanner.barcodeReceived.disconnect(self.primaryScanner_barcodeReceived)
        self.centralWindow.secondaryScanner.barcodeReceived.disconnect(self.secondaryScanner_barcodeReceived)
        print('This widget is being hidden. Handle anything necessary. Main Window')

    @pyqtSlot(bool, bool)
    def on_ManualAddButton_clicked(self, checked, longPressed):
        self.parent().setCurrentIndex(WindowType.Favorites)

    @pyqtSlot(bool, bool)
    def on_PurchaseHistoryButton_clicked(self, checked, longPressed):
        self.parent().setCurrentIndex(WindowType.PurchaseHistory)

    @pyqtSlot(bool, bool)
    def on_SettingsButton_clicked(self, checked, longPressed):
        self.centralWindow.close()

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

    @pyqtSlot(bool, bool)
    def on_printShoppingListButton_clicked(self, checked, longPressed):
        self.floatingPB1.setEnabled(True)
        self.floatingPB1.show()
        #self.reqItemsWidget.itemClicked(self,QListWidgetItem)

    @pyqtSlot()
    def selectItem(self):
        hasSelection = not self.sender().selection().isEmpty()
        self.addBtn.setEnabled(hasSelection)
        self.removeBtn.setEnabled(hasSelection)

    # Make the buttons at bottom of the screen floating; this cannot be done in Qt Designer
    # Remove the widget containing the floating buttons from the layout since Qt Designer does not allow this
    # Then setGeometry on the widget and finally raise the widget so it has a higher z-order than rest of items
  #