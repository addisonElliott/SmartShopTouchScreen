from BarcodeAPI.dataBaseManager import DataBaseManager

# Test init for connecting to DB
dbManager = DataBaseManager()
# Test Cache UPC retrieval method
cachedUPCs = dbManager.GetListOfCachedUPCs()


print("")
