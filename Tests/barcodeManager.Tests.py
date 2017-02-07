from BarcodeAPI.barcodeManager import BarcodeManager

bcManager = BarcodeManager()
# Test IsCached (Should be True)
isCached = bcManager.IsCached("070360002372")

# Test 3rd Party Json retrieval
data = bcManager.GetJsonFrom3rdParty("070360002372")
dataOkay = data["status"]["code"] == "200"

print("")
