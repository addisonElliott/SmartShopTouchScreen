import urllib.request  # For internet operations
import json  # To internet JSON data format
from Util.databaseManager import DatabaseManager
from Windows.ExpirationBox import *
from Windows.NewItemDetails import NewItemDetails


class BarcodeManager:
    def __init__(self, dbManager, config):
        self.dbManager = dbManager
        self.expBox = ExpirationBox(config)
        self.newItemDetails = NewItemDetails(config)

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
        data = self.GetJsonFrom3rdParty(barcode)
        item = {}
        if data['status']['code'] == '200':
            product = data['product']['attributes']['product']
            self.newItemDetails.itemName_textBox.setText(product[:max(20, len(product))])
            category = data['product']['attributes']['category_text']
            # TODO: Add constant dictionary of categories, check if returned category is in dictionary.
            # If it is, set combobox selected item to the key int,
            # if not, add category to dictionary with next key and add to combobox at index then select it.

        if self.newItemDetails.exec():
            item['name'] = self.newItemDetails.itemName_textBox
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

    def RemoveFromInventory(self, barcode, qty=1):
        self.dbManager.DecrementQuantityForItem(barcode, qty)

    def DisplayExpirationBox(self):
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
