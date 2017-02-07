import psycopg2


class DataBaseManager:

    def __init__(self):
        #try:
        self.connection = psycopg2.connect(database="smartshop", user="jacob", password="password", host="addison404project.ddns.net", port="5432")
        #except:
         #   raise "Cannot Connect to DataBase"

        self.cursor = self.connection.cursor()

    def GetListOfCachedUPCs(self):
        self.cursor.execute("""SELECT upc,item FROM cached_upcs""")

        return self.cursor.fetchall()
