from Windows import manualAddDialog_ui
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Util import scroller
from Util.enums import *
from Windows.virtualKeyboard import *
from Util import constants
import logging

logger = logging.getLogger(__name__)


class ManualAddDialog(QDialog, manualAddDialog_ui.Ui_ManualAddDialog):
    newCategoryText = 'newCategory'
    warningItemExists = 'Item Already Exists!'

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

        self.warningLabel.setText("")

    def updateCategories(self):
        self.categoryComboBox.clear()

        for category in self.categories:
            self.categoryComboBox.addItem(category['name'], category['id'])
        self.categoryComboBox.addItem('<New Category>', self.newCategoryText)

    @pyqtSlot(int)
    def on_categoryComboBox_currentIndexChanged(self, index):
        # If the user data is equal to the new category text identifier, then this is the New Category option selected
        if self.categoryComboBox.currentData() == self.newCategoryText:
            virtualKb = VirtualKeyboard(self)
            virtualKb.lineEdit.setMaxLength(constants.maxCategoryNameLength)

            # If the user successfully closes the keyboard, then add the category
            if virtualKb.exec() == QDialog.Accepted:
                categoryID = self.dbManager.AddCategory(virtualKb.text)

                # Query db for categories since a new one was added, update combobox since new category added
                self.categories = self.dbManager.GetCategories(True)
                self.updateCategories()

                # Find the index with the user data for the new categoryID, then set the currentIndex to that
                self.categoryComboBox.setCurrentIndex(self.categoryComboBox.findData(categoryID))
            else:
                # Set current index to be the added category
                self.categoryComboBox.setCurrentIndex(self.categoryComboBox.count() - 2)

    @pyqtSlot(str)
    def on_nameEdit_textChanged(self, str):
        # When text changes, check if the item exists and give the user a warning if it does
        # Otherwise, remove the warning if it is present already
        if self.dbManager.itemExists(str):
            self.warningLabel.setText(self.warningItemExists)
        else:
            self.warningLabel.setText("")

    @pyqtSlot(bool, bool)
    def on_confirmBtn_clicked(self, checked, longPressed):
        if (self.categoryComboBox.currentIndex() >= 0 and self.categoryComboBox.currentIndex() < len(self.categories)) \
            and (len(self.nameEdit.text()) > 0) and not self.dbManager.itemExists(self.nameEdit.text):
            self.accept()
        else:
            logger.warning("Invalid information entered into manual add dialog box. Four possible issues: no category "
                           "selected, no item name entered, or the item name already exists in the database")

    @pyqtSlot(bool, bool)
    def on_cancelBtn_clicked(self, checked, longPressed):
        self.close()