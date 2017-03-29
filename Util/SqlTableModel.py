from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from psycopg2.extensions import AsIs
import psycopg2
import datetime
from decimal import Decimal


class SqlTableModel(QAbstractTableModel):
    def __init__(self, connection, tableName = None, columnSortName = None, columnSortOrder = None, filter = None,
                 filterArgs = [], fields = None, parent = None):
        super(SqlTableModel, self).__init__(parent)

        self.tableName = tableName
        self.columnSortName = columnSortName
        self.columnSortOrder = columnSortOrder
        self.filter = filter
        self.filterArgs = filterArgs
        self.fields = fields

        self.connection = connection
        # Create cursor for SqlTableModel
        self.cursor = self.connection.cursor()

        self.resdata = []
        self.header = []

        # Execute the select statement if a table name was given
        if tableName is not None:
            self.select()

    def select(self):
        sql = self.selectStatement(False)
        if sql is None:
            return False

        self.beginResetModel()
        self.cursor.execute(sql, self.filterArgs)

        self.resdata = self.cursor.fetchall()
        self.header = [desc[0] for desc in self.cursor.description]
        self.endResetModel()
        return True

    def setTable(self, name):
        try:
            self.cursor.execute("SELECT * FROM %s", (AsIs(name),))
            self.cursor.fetchall()
            self.tableName = name
        except psycopg2.Error:
            print('Invalid table name %s' % name)

        # Commit connection in case an exception occurred
        self.connection.commit()

    def setSort(self, column, order):
        self.columnSortName = column
        self.columnSortOrder = order

    def setFilter(self, filter, filterArgs = []):
        self.filter = filter
        self.filterArgs = filterArgs

    # Contains a list of column names that the query should retrieve. If None, then set to all columns (*)
    def setFields(self, fields):
        self.fields = fields

    def selectStatement(self, runTwice = True):
        if self.tableName is None:
            print('No table name. Cannot get select statement')
            return None

        filter = ''
        orderByClause = ''
        fields = ''

        if self.filter is not None:
            filter = ' WHERE ' + self.filter

        if self.columnSortName is not None and self.columnSortOrder is not None:
            orderByClause = ' ORDER BY ' + self.columnSortName
            orderByClause += (' ASC' if self.columnSortOrder == Qt.AscendingOrder else ' DESC')

        if self.fields is None:
            fields = '*'
        else:
            fields = ','.join(self.fields)

        # Run through the statement once. Run it through again because the filter string might have additional arguments
        # to add in (filterArgs)
        firstRun = self.cursor.mogrify("SELECT %s FROM %s%s%s", (AsIs(fields), AsIs(self.tableName), AsIs(filter),
                                                               AsIs(orderByClause)))

        if runTwice:
            return self.cursor.mogrify(firstRun, self.filterArgs)
        else:
            return firstRun

    def rowCount(self, parent):
        return len(self.resdata)

    def columnCount(self, parent):
        return len(self.header)

    def data(self, index, role):
        if role != Qt.DisplayRole:
            return QVariant()

        val = self.resdata[index.row()][index.column()]

        if val is None:
            return QVariant("NULL")
        elif isinstance(val, Decimal):
            # make sure to convert special classes (otherwise it is user type in QVariant)
            return QVariant(str(val))
        elif isinstance(val, datetime.datetime):
            return QVariant(str(val))
        else:
            return QVariant(val)

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return QVariant()

        if orientation == Qt.Vertical:
            # header for a row
            return QVariant(section + 1)
        else:
            # header for a column
            return QVariant(self.header[section])