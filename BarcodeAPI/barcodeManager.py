import urllib.request  # For internet operations
import json  # To internet JSON data format
from Windows.ExpirationBox import *
from Windows.NewItemDetails import *
from Windows.CheckOutBox import *


class BarcodeManager:
    def __init__(self, dbManager, config):
        self.dbManager = dbManager
        self.expBox = ExpirationBox(config)
        categories = self.dbManager.GetCategories('ASC')
        self.newItemDetails = NewItemDetails(config, categories)
        self.checkOutBox = CheckOutBox(config)

    def AddItemToInventory(self, barcode):
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
        self.newItemDetails.ResetToDefault()
        data = self.GetJsonFrom3rdParty(barcode)
        item = {}
        if data['status']['code'] == '200':
            product = data['product']['attributes']['product']
            self.newItemDetails.itemName_textBox.setText(product[:max(20, len(product))])
            isFound = False
            if 'category_text' in data['product']['attributes']:
                category = data['product']['attributes']['category_text']
                cat_lower = category.lower()
                for index in range(0, self.newItemDetails.category_combo.count() - 1):
                    item_lower = self.newItemDetails.category_combo.itemText(index).lower()
                    if cat_lower == item_lower:
                        isFound = True
                        self.newItemDetails.category_combo.setCurrentIndex(index)
                        break

                if not isFound:
                    self.newItemDetails.category_combo.addItem(category)
                    self.newItemDetails.category_combo.setCurrentIndex(self.newItemDetails.category_combo.count() - 1)
                    self.dbManager.AddCategory(category, self.newItemDetails.category_combo.count())

        if self.newItemDetails.exec():
            item['name'] = self.newItemDetails.itemName_textBox.text()
            item['category'] = self.newItemDetails.category_combo.currentIndex()
            item['qty'] = int(self.newItemDetails.itemQty_combo.currentText())
            item['pkgQty'] = int(self.newItemDetails.pkgQty_combo.currentText())
            if self.newItemDetails.favorites_check.isChecked():
                item['favoritesIndex'] = self.dbManager.GetFavoritesCount() + 1
            expirationDate = ''
            month = self.newItemDetails.month_combo.currentText()
            day = self.newItemDetails.day_combo.currentText()
            year = self.newItemDetails.year_combo.currentText()

            if month != '' and \
               day != '' and \
               year != '':
                expirationDate = str(datetime(month=int(month), day=int(day), year=int(year)).date())

            item['expirationDate'] = expirationDate
            id = self.dbManager.AddItemToInventory(item)
            self.dbManager.AddUPCToCachedUPCs(barcode, id, item['pkgQty'])

    def RemoveFromInventory(self, barcode):
        self.checkOutBox.ResetToDefault()
        id = self.dbManager.GetCachedUPCItem(barcode)[0]
        item = self.dbManager.GetItemFromInventory(id)
        self.checkOutBox.qty_combo.setCurrentIndex(0)
        self.checkOutBox.item_textBox.setEnabled(True)
        itemName = (item[3][:20] + '..') if len(item[3]) > 20 else item[3]
        self.checkOutBox.item_textBox.setText('')
        self.checkOutBox.item_textBox.setText(itemName)
        self.checkOutBox.item_textBox.setDisabled(True)
        if self.checkOutBox.exec():
            decQty = self.checkOutBox.qty_combo.currentText()
            self.dbManager.DecrementQuantityForItem(id, item[0], int(decQty))

    def DisplayExpirationBox(self):
        self.expBox.ResetToDefault()
        expirationDate = ''
        quantity = 1
        if self.expBox.exec():
            month = self.expBox.month_combo.currentText()
            day = self.expBox.day_combo.currentText()
            year = self.expBox.year_combo.currentText()

            if month != '' and \
               day != '' and \
               year != '':
                expirationDate = str(datetime(month=int(month), day=int(day), year=int(year)).date())

            quantity = int(self.expBox.qty_combo.currentText())

        return expirationDate, quantity
