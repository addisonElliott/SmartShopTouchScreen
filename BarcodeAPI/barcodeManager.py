import urllib.request  # For internet operations
import json  # To internet JSON data format
from Util.databaseManager import DatabaseManager
from Windows.ExpirationBox import *
from Windows.NewItemDetails import NewItemDetails


class BarcodeManager:
    def __init__(self, dbManager, config, centralWindow):
        self.dbManager = dbManager
        self.config = config
        self.centralWindow = centralWindow

    def AddItemToInventory(self, barcode):
        # Strip whitespace from barcode
        barcode = barcode.strip()
        cachedItem = self.dbManager.GetCachedUPCItem(barcode)

        if cachedItem is not None:
            expirationDate, quantity = self.DisplayExpirationBox()
            self.dbManager.UpdateItemInDatabase(cachedItem, expirationDate, quantity)
        else:
            self.AddItemToDatabase(barcode)

    def CheckOutItemInInventory(self, barcode):
        item = self.dbManager.GetCachedUPCItem(barcode)
        self.CheckOutItemInInventory(item)

    def GetJsonFrom3rdParty(self, barcode):
        api = 'http://eandata.com/feed/?v=3&keycode=C9906FA4582B60E9&mode=json&find=' + barcode
        page = urllib.request.urlopen(api)
        pageString = page.read().decode('utf-8')
        data = json.loads(pageString)

        return data

    def AddItemToDatabase(self, barcode):
        categories = self.dbManager.GetCategories(True)
        newItemDetailsDialog = NewItemDetails(self.dbManager, self.config, categories, self.centralWindow)

        data = self.GetJsonFrom3rdParty(barcode)
        item = {}
        if data['status']['code'] == '200' and 'attributes' in data['product'] and 'product' in data['product']['attributes']:
            product = data['product']['attributes']['product']
            newItemDetailsDialog.itemName_textBox.setText(product[:min(constants.maxItemNameLength, len(product))])
            if 'category_text' in data['product']['attributes']:
                isFound = False
                category = data['product']['attributes']['category_text']

                # Search for a category name that is the same as category
                index = newItemDetailsDialog.category_combo.findText(category.lower(), Qt.MatchFixedString)
                if index != -1:
                    newItemDetailsDialog.category_combo.setCurrentIndex(index)
                else:
                    # If the category was not found, then add it to the combo box with an asterisk meaning it is not
                    # in the database yet. The category will only be added if that user selects that as their category
                    newItemDetailsDialog.pending_category = category
                    newItemDetailsDialog.updateCategories()
                    newItemDetailsDialog.category_combo.setCurrentIndex(newItemDetailsDialog.category_combo.findData(newItemDetailsDialog.pendingCategoryText))

                    #newItemDetailsDialog.category_combo.addItem(category)
                    #newItemDetailsDialog.category_combo.setCurrentIndex(newItemDetailsDialog.category_combo.count() - 1)
                    #self.dbManager.AddCategory(category, newItemDetailsDialog.category_combo.count())

        if newItemDetailsDialog.exec():
            item['name'] = newItemDetailsDialog.itemName_textBox.text()
            item['category'] = newItemDetailsDialog.category_combo.currentData()
            # The user selected the pending item and thus we now add it to the database
            if item['category'] == newItemDetailsDialog.pendingCategoryText:
                newCategory = newItemDetailsDialog.category_combo.currentText()[2:] # Remove * from beginning
                self.dbManager.AddCategory(newCategory)

            item['qty'] = int(newItemDetailsDialog.itemQty_combo.currentText())
            item['pkgQty'] = int(newItemDetailsDialog.pkgQty_combo.currentText())

            if newItemDetailsDialog.favorites_check.isChecked():
                index = self.dbManager.GetFavoritesCount()
                if index is None:  # If the values are all NULL, set to 0
                    index = 0

                index += 1  # Increment index by 1
                item['favoritesIndex'] = index

            expirationDate = ''
            month = newItemDetailsDialog.month_combo.currentText()
            day = newItemDetailsDialog.day_combo.currentText()
            year = newItemDetailsDialog.year_combo.currentText()

            if month and day and year:
                expirationDate = str(datetime(month=int(month), day=int(day), year=int(year)).date())

            item['expirationDate'] = expirationDate
            id = self.dbManager.AddItemToInventory(item)
            self.dbManager.AddUPCToCachedUPCs(barcode, id, item['pkgQty'])

    def RemoveFromInventory(self, barcode, qty=1):
        self.dbManager.DecrementQuantityForItem(barcode, qty)

    def DisplayExpirationBox(self):
        expirationBoxDialog = ExpirationBox(self.config, self.centralWindow)
        expirationDate = ''
        quantity = 1
        if expirationBoxDialog.exec():
            month = expirationBoxDialog.month_combo.currentText()
            day = expirationBoxDialog.day_combo.currentText()
            year = expirationBoxDialog.year_combo.currentText()

            if month and day and year:
                expirationDate = str(datetime(month=int(month), day=int(day), year=int(year)).date())

            quantity = int(expirationBoxDialog.qty_combo.currentText())

        return expirationDate, quantity
