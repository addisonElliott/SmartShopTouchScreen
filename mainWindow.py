import mainWindow_ui
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtCore import *


class MainWindow(QMainWindow, mainWindow_ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # Remove title bar to
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Sets position to 0,0 on screen and sets window to fixed size
        self.setGeometry(0, 0, 800, 480)

    @pyqtSlot()
    def keyPressEvent(self, event):
        # Pressing escape will kill the application since the title bar is absent
        if event.key() == Qt.Key_Escape:
            self.close()
