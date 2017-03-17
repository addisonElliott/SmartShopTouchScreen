from BarcodeAPI.databaseManager import DatabaseManager

# Test init for connecting to DB
dbManager = DatabaseManager()
# Test Cache UPC retrieval method
cachedUPC = dbManager.GetCachedItem("070360002372")


print("")
