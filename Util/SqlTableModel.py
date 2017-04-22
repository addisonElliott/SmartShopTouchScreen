from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from psycopg2.extensions import AsIs
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime, date
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class SqlTableModel(QAbstractTableModel):
    def __init__(self, connection, tableName = None, columnSortName = None, columnSortOrder = None, filter = None,
                 filterArgs = [], fields = None, displayColumnMapping = None, displayHeaders = None, customQuery = None,
                 limitCount = None, hideItems = False, parent = None):
        super(SqlTableModel, self).__init__(parent)

        self.tableName = tableName
        self.columnSortName = columnSortName
        self.columnSortOrder = columnSortOrder
        self.filter = filter
        self.filterArgs = filterArgs
        self.fields = fields
        self.displayColumnMapping = displayColumnMapping
        self.displayHeaders = displayHeaders
        self.customQuery = customQuery
        self.limitCount = limitCount
        self.columnAlignment = None
        self.hideItems = hideItems

        self.connection = connection
        # Create cursor for SqlTableModel
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        self.resdata = []
        self.header = []

        # Execute the select statement if a table name was given or a custom query was given
        # If the select statement is executed, initialize the columnAlignment array to be all left-aligned
        if tableName is not None or customQuery is not None:
            self.select()
            self.columnAlignment = [Qt.AlignLeft] * self.columnCount()

    def select(self):
        sql = self.selectStatement(False)
        if sql is None:
            return False

        self.beginResetModel()
        if self.hideItems:
            self.resdata = []
            self.header = []
        else:
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
        if isinstance(column, int):
            column = self.getColumnName(column)

        self.columnSortName = column
        self.columnSortOrder = order

    def setFilter(self, filter, filterArgs = []):
        self.filter = filter
        self.filterArgs = filterArgs

    # Contains a list of column names that the query should retrieve. If None, then set to all columns (*)
    def setFields(self, fields):
        self.fields = fields

    def setLimitCount(self, limitCount):
        self.limitCount = limitCount

    def setDisplayColumnMapping(self, displayColumnMapping):
        self.displayColumnMapping = displayColumnMapping

    def setDisplayHeaders(self, displayHeaders):
        self.displayHeaders = displayHeaders

    def setCustomQuery(self, query = None):
        self.customQuery = query

    def setColumnAlignment(self, column, alignment):
        if column >= 0 and column < self.columnCount():
            self.columnAlignment[column] = alignment

    def getColumnName(self, column):
        return self.header[column] if self.displayColumnMapping is None else self.header[self.displayColumnMapping[column]]

    def getSelectedRecord(self, index):
        if not index.isValid() and index.row() >= len(self.resdata):
            return None

        return self.resdata[index.row()]

    def getSelectedRecords(self, indexes):
        records = []
        for index in indexes:
            if index.isValid() and index.row() < len(self.resdata):
                records.append(self.resdata[index.row()])

        return records

    def selectStatement(self, runTwice = True):
        if self.tableName is None and self.customQuery is None:
            logger.debug("Cannot retrieve select statement with no table name AND no custom query.")
            return None

        limitClause = ''
        orderByClause = ''
        filter = ''
        fields = ''

        if self.limitCount is not None:
            limitClause = '  LIMIT ' + str(self.limitCount)

        if self.columnSortName is not None and self.columnSortOrder is not None:
            orderByClause = ' ORDER BY ' + self.columnSortName
            orderByClause += (' ASC' if self.columnSortOrder == Qt.AscendingOrder else ' DESC')

        # If sorting is enabled, then we still want to append the ORDER clause to the custom query; thus, return the
        # custom query concatenated with the order by clause
        if self.customQuery is not None:
            # We can safely use + to concatenate the strings because orderByClause is safe (cannot be SQL injected)
            return self.customQuery + orderByClause + limitClause

        if self.filter is not None:
            filter = ' WHERE ' + self.filter

        if self.fields is None:
            fields = '*'
        else:
            fields = ','.join(self.fields)

        # Run through the statement once. Run it through again because the filter string might have additional arguments
        # to add in (filterArgs)
        firstRun = self.cursor.mogrify("SELECT %s FROM %s%s%s%s", (AsIs(fields), AsIs(self.tableName), AsIs(filter),
                                                               AsIs(orderByClause), AsIs(limitClause)))

        if runTwice:
            return self.cursor.mogrify(firstRun, self.filterArgs)
        else:
            return firstRun

    def sort(self, column, order = None):
        self.setSort(column, order)
        self.select()

    def rowCount(self, parent = None):
        return len(self.resdata)

    def columnCount(self, parent = None):
        return len(self.header) if self.displayColumnMapping is None else len(self.displayColumnMapping)

    def data(self, index, role = None):
        if role == Qt.TextAlignmentRole and self.columnAlignment is not None:
            return self.columnAlignment[index.column()]

        if role != Qt.DisplayRole:
            return None

        columnIndex = index.column() if self.displayColumnMapping is None else self.displayColumnMapping[index.column()]
        val = self.resdata[index.row()][columnIndex]

        if val is None:
            return None
        elif isinstance(val, Decimal):
            # make sure to convert special classes (otherwise it is user type in QVariant)
            return str(val)
        elif isinstance(val, date):
            return str(val)
        elif isinstance(val, datetime):
            return str(val)
        else:
            return val

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Vertical:
            # header for a row
            return section + 1
        else:
            # header for a column
            if self.displayHeaders is not None:
                return self.displayHeaders[section]
            else:
                return self.getColumnName(section)