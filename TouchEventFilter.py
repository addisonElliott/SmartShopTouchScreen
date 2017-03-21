from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtGui
from PyQt5.QtCore import *
from datetime import *

class TouchEventFilter(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.HoverMove:
            mousePosition = event.pos()
            cursor = QtGui.QCursor()

            #print("[%s] Mouse moved: M[%i %i] C[%i %i]" % (datetime.now(), mousePosition.x(), mousePosition.y(), cursor.pos().x(), cursor.pos().y()))
            #return True
        elif event.type() == QEvent.Enter:
            i = 2
            #return True
        elif event.type() == QEvent.Leave:
            i = 2
            #return True
        elif event.type() == QEvent.MouseButtonPress:
            mousePosition = event.pos()
            print("[%s] Mouse pressed: %i [%i %i]" % (datetime.now(), event.button(), mousePosition.x(), mousePosition.y()))
        elif event.type() == QEvent.MouseButtonRelease:
            mousePosition = event.pos()
            print("[%s] Mouse released: %i [%i %i]" % (datetime.now(), event.button(), mousePosition.x(), mousePosition.y()))
        elif event.type() == QEvent.HoverEnter:
            print("[%s] Hover Enter" % (datetime.now()))
            #return True
        elif event.type() == QEvent.HoverLeave:
            print("[%s] Hover Leave" % (datetime.now()))
            #return True
        elif event.type() == QEvent.HoverMove:
            print("[%s] Hover Move" % (datetime.now()))
            #return True
        elif event.type() == QEvent.DragEnter:
            print("[%s] Drag Enter" % (datetime.now()))
        elif event.type() == QEvent.DragLeave:
            print("[%s] Drag Leave" % (datetime.now()))
        elif event.type() == QEvent.DragMove:
            print("[%s] Drag Move" % (datetime.now()))

        return False