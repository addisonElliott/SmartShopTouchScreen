import urllib.request  # For internet operations
import json  # To internet JSON data format
from Windows.ExpirationBox import *
from Windows.NewItemDetails import *
from Windows.CheckOutBox import *


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
            expirationDate, quantity, callbackFunction, callbackParam = \
                            self.DisplayExpirationBox(self.dbManager.getItemName(cachedItem['item']))
            self.dbManager.UpdateItemInDatabase(cachedItem, expirationDate, quantity)

            if callbackFunction and callbackParam:
                callbackFunction(callbackParam)
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
            if 'category_text' in data['product']['attributes']:
                category = data['product']['attributes']['category_text']

                # Search for a category name that is the same as category
                index = newItemDetailsDialog.category_combo.findText(category.lower(), Qt.MatchFixedString)
                if index != -1:
                    # Only change the index of the combo box if it is enabled. The combo box will not be enabled if the
                    # text entered matches a name already into the database and so it will be set to that and disabled
                    if newItemDetailsDialog.category_combo.isEnabled():
                        newItemDetailsDialog.category_combo.setCurrentIndex(index)
                else:
                    # If the category was not found, then add it to the combo box with an asterisk meaning it is not
                    # in the database yet. The category will only be added if that user selects that as their category
                    newItemDetailsDialog.pending_category = category
                    newItemDetailsDialog.updateCategories()

                    # Only change the index of the combo box if it is enabled. The combo box will not be enabled if the
                    # text entered matches a name already into the database and so it will be set to that and disabled
                    if newItemDetailsDialog.category_combo.isEnabled():
                        newItemDetailsDialog.category_combo.setCurrentIndex(newItemDetailsDialog.category_combo.findData(newItemDetailsDialog.pendingCategoryText))

            product = data['product']['attributes']['product']
            newItemDetailsDialog.itemName_textBox.setText(product[:min(constants.maxItemNameLength, len(product))])

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

            # Now that we have the information from the dialog box, we are going to do a basic check to see if the item
            # name exists in inventory already.
            existingItem = self.dbManager.GetItemFromInventory(name=item['name'])
            if existingItem:
                # If the item does exist already, then set the id to be the existing item ID
                # Also, update the existing item in inventory with new expiration date and increment quantity
                id = existingItem['item']
                cachedItem = {'item': id, 'pkg_qty': item['pkgQty']}
                self.dbManager.UpdateItemInDatabase(cachedItem, item['expirationDate'], item['qty'])
            else:
                # Otherwise, add the item to inventory based on the information entered and get the id
                id = self.dbManager.AddItemToInventory(item)

            self.dbManager.AddUPCToCachedUPCs(barcode, id, item['pkgQty'])

    def RemoveFromInventory(self, barcode):
        checkOutBox = CheckOutBox(self.config, self.centralWindow, self.centralWindow)

        cachedUPC = self.dbManager.GetCachedUPCItem(barcode)
        item = self.dbManager.GetItemFromInventory(cachedUPC['item'])

        checkOutBox.qty_combo.setCurrentIndex(0)
        checkOutBox.item_textBox.setText(item['name'])
        if checkOutBox.exec():
            decQty = checkOutBox.qty_combo.currentText()
            self.dbManager.DecrementQuantityForItem(cachedUPC['item'], int(decQty) * cachedUPC['pkg_qty'])

    def DisplayExpirationBox(self, name):
        expirationBoxDialog = ExpirationBox(self.config, self.centralWindow, name, self.centralWindow)
        expirationDate = ''
        quantity = 1
        callbackFunction = None
        callbackParam = None
        if expirationBoxDialog.exec():
            month = expirationBoxDialog.month_combo.currentText()
            day = expirationBoxDialog.day_combo.currentText()
            year = expirationBoxDialog.year_combo.currentText()

            if month and day and year:
                expirationDate = str(datetime(month=int(month), day=int(day), year=int(year)).date())

            quantity = int(expirationBoxDialog.qty_combo.currentText())
        else:
            callbackFunction = expirationBoxDialog.callbackFunction
            callbackParam = expirationBoxDialog.callbackParam

        return expirationDate, quantity, callbackFunction, callbackParam
