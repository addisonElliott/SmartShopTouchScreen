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
