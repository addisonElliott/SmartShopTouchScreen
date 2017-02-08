import urllib.request  # For internet operations
import json  # To internet JSON data format
from .databaseManager import DatabaseManager


class BarcodeManager:
    def __init__(self):
        self.dbManager = DatabaseManager()

    def AddItemToInventory(self, barcode):
        cachedItem = self.dbManager.GetCachedUPCItem()

        if cachedItem is not None:
            self.UpdateItemInDataBase(cachedItem)
        else:
            self.AddItemToDatabase(barcode)

    def GetJsonFrom3rdParty(self, barcode):
        api = "http://eandata.com/feed/?v=3&keycode=C9906FA4582B60E9&mode=json&find=" + barcode
        page = urllib.request.urlopen(api)
        pageString = page.read().decode('utf-8')
        data = json.loads(pageString)

        return data

    def UpdateItemInDataBase(self, barcode):
        query = ""

    def AddItemToDatabase(self, barcode):
        data = self.GetJsonFrom3rdParty(barcode)
