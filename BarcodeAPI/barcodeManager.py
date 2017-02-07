import urllib.request  # For internet operations
import json  # To internet JSON data format
from .dataBaseManager import DataBaseManager

dbManager = DataBaseManager()


class BarcodeManager:
    #def AddItemToInventory(barcode):
        #if IsCached(barcode):
            #
        #else:
            # add to list of items to grab from database

    def IsCached(self, barcode):
        cachedBarcodes = dbManager.GetListOfCachedUPCs()
        if barcode in (item[0] for item in cachedBarcodes):
            return True

        return False

    def GetJsonFrom3rdParty(self, barcode):
        api = "http://eandata.com/feed/?v=3&keycode=C9906FA4582B60E9&mode=json&find=" + barcode
        page = urllib.request.urlopen(api)
        pageString = page.read().decode('utf-8')
        data = json.loads(pageString)

        return data

    # def UpdateItemInDataBase(self, barcode):
