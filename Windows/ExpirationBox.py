import ExpirationBox_ui
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ExpirationBox(QDialog, ExpirationBox_ui.Ui_ExpirationBox):
    def __init__(self, config, parent=None):
        super(ExpirationBox, self).__init__(parent)
        self.setupUi(self)

        self.config = config
        # Remove title bar
        self.setWindowFlags(Qt.FramelessWindowHint)
