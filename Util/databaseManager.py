import psycopg2
from psycopg2.extensions import AsIs
from psycopg2.extras import DictCursor
import psycopg2.extras
import os
import pickle
from datetime import datetime

class DatabaseManager:
    def __init__(self, database, username, password, host, port):
        try:
            self.connection = psycopg2.connect(database=database, user=username, password=password, host=host, port=port)
        except:
            raise Exception('Cannot Connect to Database')

        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def GetCachedUPCItem(self, barcode):
        self.cursor.execute("SELECT item,pkg_qty FROM cached_upcs WHERE upc = %s", (barcode,))

        return self.cursor.fetchone()

    def GetItemFromInventory(self, id):
        self.cursor.execute("SELECT qty,avg_shelf_time,last_buy_date FROM inventory WHERE item = %s", (id,))

        return self.cursor.fetchone()

    def AddItemToInventory(self, item):
        if not 'name' in item:
            print('A valid item name must be given to add item to inventory')
            # TODO Change to logger since print wont be seen in production
            return -1

        if not 'category' in item:
            item['category'] = 1

        if not 'qty' in item:
            item['qty'] = 0

        if not 'pkgQty' in item:
            item['pkgQty'] = 0

        if not 'favoritesIndex' in item:
            item['favoritesIndex'] = None

        if not 'expirationDate' in item:
            item['expirationDate'] = None

        self.cursor.execute("INSERT INTO inventory (name, qty, category, favorites_index, expiration) VALUES "
                            "(%s, %s, %s, %s, %s) RETURNING item",
                            (item['name'], item['qty'] * item['pkgQty'], item['category'], item['favoritesIndex'],
                             item['expirationDate']))
        id = self.cursor.fetchone()[0]
        self.connection.commit()

        return id

    def AddUPCToCachedUPCs(self, barcode, id, pkgQty):
        self.cursor.execute("INSERT INTO cached_upcs (upc, item, pkg_qty) VALUES (%s, %s, %s)", (barcode, id, pkgQty))
        self.connection.commit()

    def UpdateItemInDatabase(self, cachedItem, expirationDate, quantity):
        inventoryItem = self.GetItemFromInventory(cachedItem[0])
        if expirationDate != '':
            self.cursor.execute("UPDATE inventory SET qty = %s, last_buy_date = %s, expiration = %s WHERE item = %s",
                                ((quantity * cachedItem[1]) + inventoryItem[0], str(datetime.now()),
                                expirationDate, cachedItem[0]))
        else:
            self.cursor.execute("UPDATE inventory SET qty = %s, last_buy_date = %s WHERE item = %s",
                                ((quantity * cachedItem[1]) + inventoryItem[0], str(datetime.now()), cachedItem[0]))

        self.connection.commit()

    def DecrementQuantityForItem(self, item, qty=1):
        inventoryItem = self.GetItemFromInventory(item[0])
        self.cursor.execute("UPDATE inventory SET qty = %s WHERE item = %s", (inventoryItem[0] - qty, item[0]))
        self.connection.commit()

    def AddCategory(self, name, order_index = -1):
        if order_index == -1:
            self.cursor.execute("SELECT COUNT(*) FROM category")
            numRows = self.cursor.fetchone()[0]
            order_index = numRows + 1

        self.cursor.execute("INSERT INTO category (name, order_index) VALUES (%s, %s) RETURNING id", (name, order_index))
        id = self.cursor.fetchone()[0]
        self.connection.commit()

        return id

    def GetFavoritesCount(self):
        self.cursor.execute("SELECT MAX(favorites_index) FROM inventory")

        return self.cursor.fetchone()[0]

    def GetCategory(self, id):
        self.cursor.execute("SELECT * FROM category WHERE id = %s", (id,))

        return self.cursor.fetchone()

    def GetCategories(self, order=None):
        if order is None:
            self.cursor.execute("SELECT * FROM category")
        else:
            self.cursor.execute("SELECT * FROM category ORDER BY order_index %s", (AsIs(('ASC' if order else 'DESC')),))

        return self.cursor.fetchall()

    def getUsageHistory(self, prevDateChecked=None):
        if prevDateChecked:
            self.cursor.execute("SELECT item, date, qty, (SELECT avg_usage_rate FROM inventory WHERE item = history.item) "
                                "AS avg_usage_rate FROM usage_history history WHERE date < CURRENT_DATE AND date > "
                                "DATE %s ORDER BY item, date ASC", (prevDateChecked,))
        else:
            self.cursor.execute("SELECT item, date, qty, (SELECT avg_usage_rate FROM inventory WHERE item = history.item) "
                                "AS avg_usage_rate FROM usage_history history WHERE date < CURRENT_DATE ORDER BY item, "
                                "date ASC")

        return self.cursor.fetchall()

    def updateUsageRates(self, params):
        psycopg2.extras.execute_batch(self.cursor, "UPDATE inventory SET avg_usage_rate = %s WHERE item = %s", params)

        self.connection.commit()
