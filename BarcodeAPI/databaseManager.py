import psycopg2


class DatabaseManager:

    def __init__(self):
        try:
            self.connection = psycopg2.connect(database="smartshop", user="jacob", password="password", host="addison404project.ddns.net", port="5432")
        except:
            raise Exception("Cannot Connect to Database")

        self.cursor = self.connection.cursor()

    def GetCachedUPCItem(self, barcode):
        self.cursor.execute("""SELECT item,qty FROM cached_upcs WHERE upc = """ + barcode)

        return self.cursor.fetchall()

    def GetItemFromInventory(self, id):
        self.cursor.execute("""SELECT qty,avq_qty,avg_shelf_time,last_buy_date WHERE item = """ + id)

        return self.cursor.fetchone()

    def AddItemToInventory(self, item):
        query = """INSERT INTO inventory (name, qty, avg_qty) VALUES (%s, %s, %s) RETURNING item"""
        self.cursor.execute(query, (item["name"], item["qty"], item["avgQty"]))
        id = self.cursor.fetchone()[0]
        self.connection.commit()

        return id

    def AddUPCToCachedUPCs(self, barcode, id, qty):
        query = """INSERT INTO cached_upcs (upc, item, qty) VALUES (%s, %s, %s)"""
        self.cursor.execute(query, (barcode, id, qty))
        self.connection.commit()

    def UpdateItemInDatabase(self, cachedItem):
        inventoryItem = self.GetItemFromInventory(cachedItem[0])
        query = """UPDATE inventory SET qty = %s WHERE item = %s"""
        self.cursor.execute(query, (cachedItem[1] + inventoryItem[0], cachedItem[0]))
        self.connection.commit()

    def DecrementQuantityForItem(self, item, qty=1):
        inventoryItem = self.GetItemFromInventory(item[0])
        query = """UPDATE inventory SET qty = %s WHERE item = %s"""
        self.cursor.execute(query, (inventoryItem[0] - qty, item[0]))
        self.connection.commit()
