from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Windows.virtualKeyboard import *


class TouchLineEdit(QLineEdit):
    def __init__(self, parent = None):
        super(TouchLineEdit, self).__init__(parent)
        self.autocompleteModel = None
        self.autocompleteUpdateCallback = None
        self.virtualKb = None

    def focusInEvent(self, event):
        super(TouchLineEdit, self).focusInEvent(event)

        # If the virtual keyboard is not visible or non-existent, then create it and show it
        if self.virtualKb is None or not self.virtualKb.isVisible():
            self.virtualKb = VirtualKeyboard(self, self, self.autocompleteModel)
            if self.autocompleteUpdateCallback:
                self.virtualKb.updateSuggestions.connect(self.autocompleteUpdateCallback)
            self.virtualKb.show()
            self.virtualKb.raise_()
