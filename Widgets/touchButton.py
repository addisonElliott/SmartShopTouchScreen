from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class TouchButton(QPushButton, QObject):
    # Signal is emitted once it has been selected
    pressed = pyqtSignal(bool, bool, name='clicked')

    def __init__(self, parent = None):
        super(TouchButton, self).__init__(parent)

    def mousePressEvent(self, event):
        if self.hitButton(event.pos()):
            if event.button() == Qt.LeftButton or event.button() == Qt.RightButton:
                self.setDown(True)
                event.accept()

    def mouseReleaseEvent(self, event):
        if self.hitButton(event.pos()) and self.isDown():
            if event.button() == Qt.LeftButton:
                self.pressed.emit(self.isChecked(), False)
                self.click()
            elif event.button() == Qt.RightButton:
                self.pressed.emit(self.isChecked(), True)
                self.click()

            self.repaint()
        else:
            self.setDown(False)
