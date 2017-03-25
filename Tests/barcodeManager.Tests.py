from BarcodeAPI.barcodeManager import BarcodeManager
from Util.databaseManager import *
from Util import constants

dbManager = DatabaseManager(constants.dbDatabase, constants.dbUsername, constants.dbPassword, constants.dbHost, constants.dbPort)
bcManager = BarcodeManager(dbManager)

# Test 3rd Party Json retrieval
data = bcManager.GetJsonFrom3rdParty("070360002372")
dataOkay = data["status"]["code"] == "200"

print("")
