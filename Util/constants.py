from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# This file contains all the constants that will not be regularly changed upon runtime
# It is benficial to developers who want to fine-tune or tweak some parameters to optimize some aspect of the code

# Enables/Disables the barcode scanner device. If enabled, this will actually search for the barcode scanners on the USB
# ports and try to connect with them. Only disable this for developer mode where the barcode scanners will not be used
barcodeScannerDeviceEnable = False

# Enables/Disables shortcuts for the barcode scanner. If enabled, this will allow the user to press Ctrl+1 and Ctrl+2
# which enables an input dialog box to input the barcode to be sent.
barcodeScannerShortcut = True

# Geometry for each window that is going to be displayed
windowGeometry = QRect(0, 0, 800, 480)

# Interval for polling barcode scanners in milliseconds
scannerPollInterval = 5

# Whether the menu will be shown as full screen or not
fullscreen = False

# number of years after current year for expiration date
maxExpirationYear = 25

# Database information to connect to PostgreSQL server.
dbDatabase = "smartshop"
dbUsername = "jacob"
dbPassword = "password"
dbHost = "addison404project.ddns.net"
dbPort = "5432"

# Maximum length that a category name can be
maxCategoryNameLength = 20

# Log filename, where information will be stored
logFilename = 'log.txt'
import logging
logLevel = logging.DEBUG