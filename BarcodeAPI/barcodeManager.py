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


    def IsCached(barcode):
        cachedBarcodes = dbManager.GetListOfCachedUPCs()
        if barcode in cachedBarcodes:
            return True

        return False


    def GetJsonFrom3rdParty(barcode):
        api = "http://eandata.com/feed/?v=3&keycode=C9906FA4582B60E9&mode=json&find=" + barcode
        page = urllib.urlopen(api)
        data = json.load(page)

        return data


    #def UpdateItemInDataBase(barcode):
