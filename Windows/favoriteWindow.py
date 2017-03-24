from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Windows.centralWindow import *
from Windows import favoriteWindow_ui
from Util import constants, scroller
from Util.enums import *

class FavoriteWindow(QWidget, favoriteWindow_ui.Ui_FavoriteWindow):
    def __init__(self, parent=None):
        super(FavoriteWindow, self).__init__(parent)
        self.setupUi(self)

        self.tableModel = QStandardItemModel(4, 5, self)

        self.tableModel.setItem(0, 0, QStandardItem("Rawr"))
        self.tableModel.setItem(0, 1, QStandardItem("Really Long String of Words"))
        self.tableModel.setItem(0, 2, QStandardItem("Really Long"))
        self.tableModel.setItem(0, 3, QStandardItem("POPTARTS STRAWBERRY"))
        self.tableModel.setItem(1, 0, QStandardItem("Rawr"))
        self.tableModel.setItem(1, 1, QStandardItem("OOOOOOOOOO OOOOOOOOOO"))
        self.tableModel.setItem(1, 2, QStandardItem("OOOOOOOOOO OOOOOOOOO"))
        self.tableModel.setItem(1, 3, QStandardItem("OOOOOOOOO OOOOOOOO"))
        self.tableModel.setItem(1, 4, QStandardItem("OOOOOOOO OOOOOOO"))

        self.tableView.setModel(self.tableModel)

        scroller.setupScrolling(self.tableView)

        # Setup a tab
        self.tabTest = QWidget(self.tabWidget)
        self.horizontalLayout_10 = QHBoxLayout(self.tabTest)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)

        self.listTabTest = QListView(self.tabTest)
        font = QFont()
        font.setPointSize(21)
        self.listTabTest.setFont(font)
        self.listTabTest.setFrameShape(QFrame.NoFrame)
        self.listTabTest.setFrameShadow(QFrame.Plain)
        self.listTabTest.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.listTabTest.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listTabTest.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listTabTest.setDragDropMode(QAbstractItemView.DragDrop)
        self.listTabTest.setDefaultDropAction(Qt.ActionMask)
        self.listTabTest.setAlternatingRowColors(True)
        self.listTabTest.setSelectionMode(QAbstractItemView.MultiSelection)
        self.listTabTest.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.listTabTest.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.horizontalLayout_10.addWidget(self.listTabTest)

        self.tabWidget.addTab(self.tabTest, 'Test')

        self.stringList = QStringListModel(self)
        self.stringList.setStringList(['One', 'Two', 'Three', 'Four', 'Five'])

        self.listTabTest.setModel(self.stringList)

    @pyqtSlot()
    def on_backBtn_clicked(self):
        self.parent().setCurrentIndex(WindowType.Home)

    @pyqtSlot()
    def on_homeBtn_clicked(self):
        self.parent().setCurrentIndex(WindowType.Home)