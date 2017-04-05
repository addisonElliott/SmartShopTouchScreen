from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class TouchSpinBox(QSpinBox):
    ItemHeight = 25

    def __init__(self, parent = None):
        super(TouchSpinBox, self).__init__(parent)

    def event(self, event):
        if event.type() == QEvent.ScrollPrepare:
            # Calculate content position range by getting min and max values for spin box (multiply by a factor of ItemHeight)
            min = self.minimum() * TouchSpinBox.ItemHeight
            max = self.maximum() * TouchSpinBox.ItemHeight
            height = min + max

            # Setup scroller by setting viewport size, content range and the current position
            event.setViewportSize(QSizeF(self.size()))
            event.setContentPosRange(QRectF(0.0, min, 0.0, height))
            event.setContentPos(QPointF(0.0, self.value() * TouchSpinBox.ItemHeight))
            event.accept()
            return True
        elif event.type() == QEvent.Scroll:
            self.setValue(round(event.contentPos().y() / TouchSpinBox.ItemHeight))
            event.accept()
            return True
        else:
            return super(TouchSpinBox, self).event(event)
