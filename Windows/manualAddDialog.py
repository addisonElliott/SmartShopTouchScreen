from Windows import manualAddDialog_ui
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Util import scroller
from Util.enums import *

class ManualAddDialog(QDialog, manualAddDialog_ui.Ui_ManualAddDialog):
    def __init__(self, config, dbManager, categories, parent=None):
        super(ManualAddDialog, self).__init__(parent)
        self.setupUi(self)

        self.config = config
        self.dbManager = dbManager
        self.categories = categories

        # Remove title bar
        self.setWindowFlags(Qt.FramelessWindowHint)

        scroller.setupScrolling(self.categoryComboBox.view())
        self.categoryComboBox.view().setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        scroller.setupScrolling(self.quantitySpinBox, ScrollingType.SpinBox)

        for category in self.categories:
            self.categoryComboBox.addItem(category['name'])
        self.categoryComboBox.addItem('<New Item>')

    @pyqtSlot(bool, bool)
    def on_confirmBtn_clicked(self, checked, longPressed):
        self.accept()

    @pyqtSlot(bool, bool)
    def on_cancelBtn_clicked(self, checked, longPressed):
        self.close()