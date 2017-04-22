import psycopg2
from psycopg2.extensions import AsIs
from psycopg2.extras import DictCursor
import psycopg2.extras
import os
import pickle
from datetime import datetime
from Util.exception import *


class DatabaseManager:
    def __init__(self, database, username, password, host, port):
        try:
            self.connection = psycopg2.connect(database=database, user=username, password=password, host=host, port=port)
        except:
            raise Exception('Cannot Connect to Database')

        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def GetCachedUPCItem(self, barcode):
        self.cursor.execute("SELECT item,pkg_qty FROM cached_upcs WHERE upc = %s", (barcode,))

        if self.cursor.rowcount <= 0:
            return None
        else:
            return self.cursor.fetchone()

    def getItemName(self, item):
        self.cursor.execute("SELECT name FROM inventory WHERE item = %s", (item,))

        return self.cursor.fetchone()[0]

    def itemExists(self, name):
        self.cursor.execute("SELECT COUNT(*) FROM inventory WHERE name = %s", (name,))

        return self.cursor.fetchone()[0] != 0

    def GetItemFromInventory(self, id = None, name = None):
        if id is not None:
            self.cursor.execute("SELECT * FROM inventory WHERE item = %s", (id,))
        elif name is not None:
            self.cursor.execute("SELECT * FROM inventory WHERE name = %s", (name,))
        else:
            return None

        if self.cursor.rowcount == 0:
            return None
        else:
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

        if not 'expirationDate' in item or not item['expirationDate']:
            item['expirationDate'] = None

        self.cursor.execute("INSERT INTO inventory (name, qty, category, favorites_index, expiration) VALUES "
                            "(%s, %s, %s, %s, %s) RETURNING item",
                            (item['name'], item['qty'] * item['pkgQty'], item['category'], item['favoritesIndex'],
                             item['expirationDate']))

        id = self.cursor.fetchone()[0]
        self.connection.commit()

        # Update the purchase history with item bought today
        self.updatePurchaseHistory(id, datetime.now().date(), item['qty'] * item['pkgQty'])

        return id

    def AddUPCToCachedUPCs(self, barcode, id, pkgQty):
        self.cursor.execute("INSERT INTO cached_upcs (upc, item, pkg_qty) VALUES (%s, %s, %s)", (barcode, id, pkgQty))
        self.connection.commit()

    def UpdateItemInDatabase(self, cachedItem, expirationDate, quantity):
        inventoryItem = self.GetItemFromInventory(cachedItem['item'])
        if expirationDate is '':
            expirationDate = None

        # Update the item in inventory. Only update the expiration date if the date given is more recent than the existing
        # one
        self.cursor.execute("UPDATE inventory SET qty = %(qty)s, last_buy_date = %(buy_date)s, expiration = "
                            "CASE "
                            "WHEN expiration IS NULL THEN DATE(%(expiration_date)s) "
                            "WHEN DATE(%(expiration_date)s) IS NULL THEN expiration "
                            "WHEN expiration <= DATE(%(expiration_date)s) THEN expiration "
                            "WHEN expiration > DATE(%(expiration_date)s) THEN DATE(%(expiration_date)s) "
                            "END "
                            "WHERE item = %(item)s",
                            {'qty': ((quantity * cachedItem['pkg_qty']) + inventoryItem['qty']),
                             'buy_date': str(datetime.now()), 'item': cachedItem['item'],
                             'expiration_date': expirationDate})

        self.connection.commit()

        # Update the purchase history with item bought today
        self.updatePurchaseHistory(cachedItem['item'], datetime.now().date(), quantity * cachedItem['pkg_qty'])

    def updatePurchaseHistory(self, item, date, qty):
        self.cursor.execute("DO $do$ BEGIN UPDATE purchase_history SET qty = qty + %(qty)s WHERE item = %(item)s AND "
                            "date = %(date)s; IF NOT FOUND THEN INSERT INTO purchase_history (item, date, qty) VALUES "
                            "(%(item)s, %(date)s, %(qty)s); END IF; END $do$", {'item': item, 'date': str(date),
                                                                                'qty': qty})
        self.connection.commit()

    def DecrementQuantityForItem(self, id, decQty=1):
        self.cursor.execute("UPDATE inventory SET qty = GREATEST(qty - %s, 0), expiration = %s WHERE item = %s",
                            (decQty, None, id))
        self.connection.commit()

    def AddCategory(self, name, order_index = -1):
        if order_index == -1:
            self.cursor.execute("SELECT MAX(order_index) FROM category")
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

    def removeItemFromRequiredList(self, id):
        self.cursor.execute("UPDATE inventory SET list_flags = 0 WHERE item = %s", (id,))

        self.connection.commit()

    def removeItemFromRecommendedList(self, id):
        self.cursor.execute("UPDATE inventory SET list_flags = 3 WHERE item = %s", (id,))

        self.connection.commit()

    def setRequiredItems(self, itemList):
        if isinstance(itemList, (list, tuple)):
            self.cursor.execute("UPDATE inventory SET list_flags = 1 WHERE item IN %s", (itemList,))
        else:
            self.cursor.execute("UPDATE inventory SET list_flags = 1 WHERE item = %s", (itemList,))

        self.connection.commit()

    def updateRecommendedItems(self, expirationDateThreshold, avgShelfTimeThreshold):
        # Set list flag to 2 (recommended item) for all items that meet these criteria:
        #   - List flags equals 0 meaning it is not a required item, recommended item, or ignored item.
        #   - Expiration date is within X days of today where X is the threshold set in settings
        #   OR
        #   - [Average shelf time and last buy date are not null. If they are, then that means this next calculation cant
        #   - be done.
        #   AND
        #   - Last buy date plus average shelf time is the expected time when the item will be required again. If this
        #   - is within X days of todays date, then select it. X being threshold set in settings
        if expirationDateThreshold:
            self.cursor.execute("UPDATE inventory SET list_flags = 2 WHERE item IN "
                                "(SELECT item FROM inventory WHERE list_flags = 0 AND "
                                "(expiration <= DATE(CURRENT_DATE + %s)))",
                                (expirationDateThreshold,))

        if avgShelfTimeThreshold:
            self.cursor.execute("UPDATE inventory SET list_flags = 2 WHERE item IN "
                                "(SELECT item FROM inventory WHERE list_flags = 0 AND "
                                "(avg_shelf_time IS NOT NULL AND last_buy_date IS NOT NULL AND "
                                "(last_buy_date + avg_shelf_time) <= DATE(CURRENT_DATE + %s)))",
                                (avgShelfTimeThreshold, ))

        self.connection.commit()