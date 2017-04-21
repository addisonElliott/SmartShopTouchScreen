from Windows import manualAddDialog_ui
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Util import scroller
from Util.enums import *
from Windows.virtualKeyboard import *
from Util import constants


class ManualAddDialog(QDialog, manualAddDialog_ui.Ui_ManualAddDialog):
    def __init__(self, config, dbManager, categories, currentCategory = 0, parent=None):
        super(ManualAddDialog, self).__init__(parent)
        self.setupUi(self)

        self.config = config
        self.dbManager = dbManager
        self.categories = categories

        # Remove title bar
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)

        scroller.setupScrolling(self.categoryComboBox.view())
        # Set the combobox view to scroll per pixel so the kinetic scrolling via touchscreen isnt ridiculously fast
        self.categoryComboBox.view().setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # Disabling mouse tracking means that when you first use touchscreen to scroll through items, then it wont
        # select that item
        self.categoryComboBox.view().setMouseTracking(False)

        self.updateCategories()
        self.categoryComboBox.setCurrentIndex(currentCategory)

    def updateCategories(self):
        self.categoryComboBox.clear()

        for category in self.categories:
            self.categoryComboBox.addItem(category['name'])
        self.categoryComboBox.addItem('<New Category>')

    @pyqtSlot(int)
    def on_categoryComboBox_currentIndexChanged(self, index):
        # If the selected index is the last in the list AND the text says <New Category>, then open dialog box to create
        # a new category
        if index == self.categoryComboBox.count() - 1 and self.categoryComboBox.itemText(index) == '<New Category>':
            self.virtualKb = VirtualKeyboard(self)
            self.virtualKb.lineEdit.setMaxLength(constants.maxCategoryNameLength)

            # If the user successfully closes the keyboard, then add the category
            if self.virtualKb.exec() == QDialog.Accepted:
                self.dbManager.AddCategory(self.virtualKb.text)

                # Query db for categories since a new one was added, update combobox since new category added
                self.categories = self.dbManager.GetCategories(True)
                self.updateCategories()

            # Set current index to be the added category
            self.categoryComboBox.setCurrentIndex(self.categoryComboBox.count() - 2)

    @pyqtSlot(bool, bool)
    def on_confirmBtn_clicked(self, checked, longPressed):
        if (self.categoryComboBox.currentIndex() >= 0 and self.categoryComboBox.currentIndex() < len(self.categories)) \
            and (len(self.nameEdit.text()) > 0):
            self.accept()
        else:
            print('Please enter data into all of the fields to continue')

    @pyqtSlot(bool, bool)
    def on_cancelBtn_clicked(self, checked, longPressed):
        self.close()