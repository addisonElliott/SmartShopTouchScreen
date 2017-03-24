from PyQt5.QtWidgets import QTableView, QApplication
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import *

class TileView(QTableView):
    def __init__(self, parent):
        super(TileView, self).__init__(parent)

    def mousePressEvent(self, event):
        super(TileView, self).mousePressEvent(event)

        # For a right button click, note the start position when mouse down
        if event.button() == Qt.RightButton:
            self.dragStartPosition = event.pos()

    def mouseMoveEvent(self, event):
        super(TileView, self).mouseMoveEvent(event)

        # If the button is a right click and it has moved a predetermined distance from the start point, then start
        # a drag operation
        if (event.buttons() & Qt.RightButton) and ((event.pos() - self.dragStartPosition).manhattanLength() >=
                                                       QApplication.startDragDistance()):
            # Select the current index since that is what we are wanting to drag that one most likely
            selectedItem = self.indexAt(event.pos())
            if selectedItem is not None:
                self.selectionModel().select(selectedItem, QItemSelectionModel.Select)

            self.startDrag(Qt.ActionMask)

    def dragEnterEvent(self, event):
        # If the right mouse button was clicked for this drag event, then accept it.
        if (event.mouseButtons() & Qt.RightButton):
            event.acceptProposedAction()

    def dropEvent(self, event):
        print('Drop event')
        print(event)