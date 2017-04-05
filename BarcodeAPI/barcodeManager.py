import urllib.request  # For internet operations
import json  # To internet JSON data format
from .databaseManager import DatabaseManager
from Windows.ExpirationBox import *


class BarcodeManager:
    def __init__(self):
        self.dbManager = DatabaseManager()
        self.expBox = ExpirationBox()

    def ShowExpirationBox(self):
        self.expBox.exec()

    def AddItemToInventory(self, barcode):
        cachedItem = self.dbManager.GetCachedUPCItem()

        if cachedItem is not None:
            self.dbManager.UpdateItemInDatabase(cachedItem)
        else:
            self.AddItemToDatabase(barcode)

    def CheckOutItemInInventory(self, barcode):
        item = self.dbManager.GetCachedUPCItem(barcode)
        self.CheckOutItemInInventory(item)

    def GetJsonFrom3rdParty(self, barcode):
        api = "http://eandata.com/feed/?v=3&keycode=C9906FA4582B60E9&mode=json&find=" + barcode
        page = urllib.request.urlopen(api)
        pageString = page.read().decode('utf-8')
        data = json.loads(pageString)

        return data

    def AddItemToDatabase(self, barcode):
        data = self.GetJsonFrom3rdParty(barcode)
        if data["status"]["code"] == "200":
            item = self.ParseJsonObject(data)
            id = self.dbManager.AddItemToInventory(item)
            self.dbManager.AddUPCToCachedUPCs(barcode, id, item["qty"])
        else:
            item = {}
            item["name"] = "Unknown Item"
            item["qty"] = 1
            item["avgQty"] = 1
            id = self.dbManager.AddItemToInventory(item)
            self.dbManager.AddUPCToCachedUPCs(barcode, id, item["qty"])


    def ParseJsonObject(self, data):
        item = {}
        item["name"] = data["product"]["attributes"]["product"]
        item["qty"] = 1
        item["avgQty"] = 1

        return item

    def RemoveFromInventory(self, barcode, qty=1):
        self.dbManager.DecrementQuantityForItem(barcode, qty)
