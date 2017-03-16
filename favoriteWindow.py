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

        # Make the buttons at bottom of the screen floating; this cannot be done in Qt Designer
        # Remove the widget containing the floating buttons from the layout since Qt Designer does not allow this
        # Then setGeometry on the widget and finally raise the widget so it has a higher z-order than rest of items
        self.centralwidget.layout().removeWidget(self.floatingBtnWidget)
        floatingBtnWidgetWidth = 48 * 2 + 40
        floatingBtnWidgetHeight = 48 + 12
        floatingBtnWidgetX = (self.width() - floatingBtnWidgetWidth) / 2
        floatingBtnWidgetY = self.height() - floatingBtnWidgetHeight - 1
        self.floatingBtnWidget.setGeometry(floatingBtnWidgetX, floatingBtnWidgetY, floatingBtnWidgetWidth, floatingBtnWidgetHeight)
        self.floatingBtnWidget.raise_()