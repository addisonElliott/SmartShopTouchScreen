from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# This file contains all the constants that will not be regularly changed upon runtime
# It is benficial to developers who want to fine-tune or tweak some parameters to optimize some aspect of the code

# Enables/Disables shortcuts for the barcode scanner. If enabled, this will allow the user to press Ctrl+1 and Ctrl+2
# which enables an input dialog box to input the barcode to be sent.
barcodeScannerShortcut = True

# Geometry for each window that is going to be displayed
windowGeometry = QRect(0, 0, 800, 480)

# Interval for polling barcode scanners in milliseconds
scannerPollInterval = 5