import urllib.request  # For internet operations
import json  # To internet JSON data format
from Util.databaseManager import DatabaseManager
from Windows.ExpirationBox import *

class BarcodeManager:
    def __init__(self, dbManager, config):
        self.dbManager = dbManager
        self.expBox = ExpirationBox(config)

    def AddItemToInventory(self, barcode, expirationDate, quantity):
        cachedItem = self.dbManager.GetCachedUPCItem()

        if cachedItem is not None:
            self.dbManager.UpdateItemInDatabase(cachedItem, expirationDate, quantity)
        else:
            self.AddItemToDatabase(barcode, expirationDate, quantity)

    def CheckOutItemInInventory(self, barcode):
        item = self.dbManager.GetCachedUPCItem(barcode)
        self.CheckOutItemInInventory(item)

    def GetJsonFrom3rdParty(self, barcode):
        api = "http://eandata.com/feed/?v=3&keycode=C9906FA4582B60E9&mode=json&find=" + barcode
        page = urllib.request.urlopen(api)
        pageString = page.read().decode('utf-8')
        data = json.loads(pageString)

        return data

    def AddItemToDatabase(self, barcode, expirationDate, quantity):
        data = self.GetJsonFrom3rdParty(barcode)
        if data["status"]["code"] == "200":
            item = self.ParseJsonObject(data, expirationDate, quantity)
            id = self.dbManager.AddItemToInventory(item)
            self.dbManager.AddUPCToCachedUPCs(barcode, id, item["qty"])
        else:
            item = {}
            item["name"] = "Unknown Item"
            item["qty"] = 1
            item["avgQty"] = 1
            id = self.dbManager.AddItemToInventory(item)
            self.dbManager.AddUPCToCachedUPCs(barcode, id, item["qty"])


    def ParseJsonObject(self, data, expirationDate, quantity):
        item = {}
        item["name"] = data["product"]["attributes"]["product"]
        item["qty"] = quantity
        item["avgQty"] = quantity
        item['expirationDate'] = expirationDate

        return item

    def RemoveFromInventory(self, barcode, qty=1):
        self.dbManager.DecrementQuantityForItem(barcode, qty)
