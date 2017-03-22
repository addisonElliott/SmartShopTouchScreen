import favoriteWindow_ui
from ManualAddDialog import *
from scanner import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import constants

class FavoriteWindow(QMainWindow, favoriteWindow_ui.Ui_FavoriteWindow):
    def __init__(self, config, parent=None):
        super(FavoriteWindow, self).__init__(parent)
        self.setupUi(self)

        self.config = config

        # Remove title bar
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Sets position to 0,0 on screen and sets window to fixed size
        self.setGeometry(constants.windowGeometry)

        # Create shortcut for escape key that calls close()
        self.closeShortcut = QShortcut(Qt.Key_Escape, self)
        self.closeShortcut.activated.connect(self.close)

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

        scroller = QScroller.scroller(self.tableView)
        scroller.grabGesture(self.tableView, QScroller.LeftMouseButtonGesture)

        scrollerProps = scroller.scrollerProperties()
        scrollerProps.setScrollMetric(QScrollerProperties.HorizontalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
        scrollerProps.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
        scrollerProps.setScrollMetric(QScrollerProperties.OvershootScrollDistanceFactor, 0)
        scrollerProps.setScrollMetric(QScrollerProperties.OvershootDragDistanceFactor, 0)
        scroller.setScrollerProperties(scrollerProps)

        #sp = QScrollerProperties()
        #sp.setScrollMetric(QScrollerProperties.DragVelocitySmoothingFactor, 0.6)
        #sp.setScrollMetric(QScrollerProperties.MinimumVelocity, 0.0)
        #sp.setScrollMetric(QScrollerProperties.MaximumVelocity, 0.5)
        #sp.setScrollMetric(QScrollerProperties.AcceleratingFlickMaximumTime, 0.4)
        #sp.setScrollMetric(QScrollerProperties.AcceleratingFlickSpeedupFactor, 1.2)
        #sp.setScrollMetric(QScrollerProperties.SnapPositionRatio, 0.2)
        #sp.setScrollMetric(QScrollerProperties.MaximumClickThroughVelocity, 0)
        #sp.setScrollMetric(QScrollerProperties.DragStartDistance, 0.001)
        #sp.setScrollMetric(QScrollerProperties.MousePressEventDelay, 0.5)

        #scroller = QScroller(self.tableView)

        #QScroller.grabGesture(self.tableView, QScroller.LeftMouseButtonGesture)
        #scroller.setScrollerProperties(sp)

        #self.tableView.setHorizontalScrollBarPolic(QAbstractItemView.ScrollPerPixel)
        self.tableView.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        #self.tableView.setVerticalScrollBarPolicy(QAbstractItemView.ScrollPerPixel)