import psycopg2


class DatabaseManager:

    def __init__(self):
        try:
            self.connection = psycopg2.connect(database="smartshop", user="jacob", password="password", host="addison404project.ddns.net", port="5432")
        except:
            raise Exception("Cannot Connect to Database")

        self.cursor = self.connection.cursor()

    def GetCachedUPCItem(self, barcode):
        self.cursor.execute("""SELECT item FROM cached_upcs WHERE upc = """ + barcode)

        return self.cursor.fetchall()

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
