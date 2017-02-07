from BarcodeAPI.databaseManager import DatabaseManager

# Test init for connecting to DB
dbManager = DatabaseManager()
# Test Cache UPC retrieval method
cachedUPCs = dbManager.GetListOfCachedUPCs()


print("")
