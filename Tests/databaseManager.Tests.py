from Util.databaseManager import DatabaseManager
from Util import constants

# Test init for connecting to DB
dbManager = DatabaseManager(constants.dbDatabase, constants.dbUsername, constants.dbPassword, constants.dbHost, constants.dbPort)
# Test Cache UPC retrieval method
cachedUPC = dbManager.GetCachedUPCItem("070360002372")

dbManager.GetItemFromInventory(2)


print("")
