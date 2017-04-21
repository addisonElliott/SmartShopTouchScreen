import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Util.exception import *
from Util import constants

if sys.platform.startswith("linux"):
    from evdev import *
    from evdev.ecodes import *
    import re

    keycodeToASCII = {
        KEY_1: ['1', '!'], KEY_2: ['2', '@'], KEY_3: ['3', '#'], KEY_4: ['4', '$'], KEY_5: ['5', '%'], KEY_6: ['6', '^'],
        KEY_7: ['7', '*'], KEY_8: ['8', '('], KEY_9: ['9', '('], KEY_0: ['0', ')'], KEY_MINUS: ['-', '_'], KEY_EQUAL: ['=', '+'],
        KEY_TAB: ['\t', '\t'], KEY_Q: ['q', 'Q'], KEY_W: ['w', 'W'], KEY_E: ['e', 'E'], KEY_R: ['r', 'R'], KEY_T: ['t', 'T'],
        KEY_Y: ['y', 'Y'], KEY_U: ['u', 'U'], KEY_I: ['i', 'I'], KEY_O: ['o', 'O'], KEY_P: ['p', 'P'], KEY_LEFTBRACE: ['[', '{'],
        KEY_RIGHTBRACE: [']', '}'], KEY_ENTER: ['\r\n', '\r\n'], KEY_A: ['a', 'A'], KEY_S: ['s', 'S'], KEY_D: ['d', 'D'],
        KEY_F: ['f', 'F'], KEY_G: ['g', 'G'], KEY_H: ['h', 'H'], KEY_J: ['j', 'J'], KEY_K: ['k', 'K'], KEY_L: ['l', 'L'],
        KEY_SEMICOLON: [';', ':'], KEY_APOSTROPHE: ['\'', '\"'], KEY_GRAVE: ['`', '~'], KEY_BACKSLASH: ['\\', '|'], KEY_Z: ['z', 'Z'],
        KEY_X: ['x', 'X'], KEY_C: ['c', 'C'], KEY_V: ['v', 'V'], KEY_B: ['b', 'B'], KEY_N: ['n', 'N'], KEY_M: ['m', 'M'],
        KEY_COMMA: [',', '<'], KEY_DOT: ['.', '>'], KEY_SLASH: ['/', '?'], KEY_SPACE: [' ', ' ']
    }

    numpadcodeToASCII = {
        KEY_KPASTERISK: '*', KEY_KP7: '7', KEY_KP8: '8', KEY_KP9: '9', KEY_KPMINUS: '-', KEY_KP4: '4', KEY_KP5: '5', KEY_KP6: '6',
        KEY_KPPLUS: '+', KEY_KP1: '1', KEY_KP2: '2', KEY_KP3: '3', KEY_KP0: '0', KEY_KPDOT: '.', KEY_KPSLASH: '/'
    }

    class BarcodeScanner(QObject):
        # Signal is emitted once a barcode has been scanned and received
        barcodeReceived = pyqtSignal(str)

        def __init__(self, parent, usbPortNumber, shortcut=None, scannerTitle=None):
            QObject.__init__(self, parent)
            self.parent = parent

            self.modifiers = {
                KEY_RIGHTMETA:  0,  # Right GUI - (usually the Windows key)
                KEY_RIGHTALT:   0,  # Right ALT
                KEY_RIGHTSHIFT: 0,  # Right Shift
                KEY_RIGHTCTRL:  0,  # Right Control
                KEY_LEFTMETA:   0,  # Left GUI - (again, usually the Windows key)
                KEY_LEFTALT:    0,  # Left ALT
                KEY_LEFTSHIFT:  0,  # Left Shift
                KEY_LEFTCTRL:   0   # Left Control
            }
            self.state = {
                KEY_CAPSLOCK: 0,    # Caps Lock
                KEY_NUMLOCK: 0,     # Num Lock
                KEY_SCROLLLOCK: 0,  # Scroll Lock
            }

            # Setup the device by calling setPort with the desired port number
            self.usbPortNumber = None
            self.setPort(usbPortNumber)

            # Set the current string buffer to none
            self.curStr = ""

            # Set the current string buffer to none
            if shortcut is not None:
                self.shortcut = QShortcut(shortcut, self.parent)
                self.shortcut.activated.connect(self.shortcut_activated)
                if scannerTitle:
                    self.shortcutMessage = "Enter %s barcode: " % scannerTitle
                else:
                    self.shortcutMessage = "Enter barcode: "

        def setPort(self, usbPortNumber):
            # Do nothing if the given port is the same as the current port
            if self.usbPortNumber == usbPortNumber:
                return

            if constants.barcodeScannerDeviceEnable:
                # This regex expression identifies a device on a specified USB port number
                # I am not entirely sure if this is Raspbian specific, Linux specific or what,
                # but it works in this case
                rePhysicalLoc = re.compile("usb\-.*\..*\-1\.%i.*" % usbPortNumber)

                # Loop through all available devices and search for a regex match
                # First match found is the device we will use
                devices = [InputDevice(fn) for fn in list_devices()]
                self.device = None
                for device in devices:
                    if rePhysicalLoc.match(device.phys) is not None:
                        self.device = device
                        break

                # If unable to find the device at port number, raise error
                if self.device is None:
                    raise SmartShopException("Unable to find input device located at port %i" % usbPortNumber)

                # Get the current state of the LED buttons; update self.state with the values that are on
                ledStates = self.device.leds()
                if LED_CAPSL in ledStates: self.state[KEY_CAPSLOCK] = 1
                if LED_NUML in ledStates: self.state[KEY_NUMLOCK] = 1
                if LED_SCROLLL in ledStates: self.state[KEY_SCROLLLOCK] = 1

                # Set current port number to the given port number
                self.usbPortNumber = usbPortNumber

        def poll(self):
            try:
                if constants.barcodeScannerDeviceEnable:
                    # Read all of the events from the loop
                    deviceEvents = self.device.read()

                    for event in deviceEvents:
                        # Only accept keyboard events
                        if event.type is EV_KEY:
                            keyEvent = util.categorize(event)

                            if keyEvent.scancode in self.modifiers:
                                if keyEvent.keystate is events.KeyEvent.key_down: self.modifiers[keyEvent.scancode] = 1
                                elif keyEvent.keystate is events.KeyEvent.key_up: self.modifiers[keyEvent.scancode] = 0
                            elif keyEvent.scancode in self.state:
                                if keyEvent.keystate is events.KeyEvent.key_down: self.state[keyEvent.scancode] = 1
                                elif keyEvent.keystate is events.KeyEvent.key_up: self.state[keyEvent.scancode] = 0
                            elif keyEvent.keystate is events.KeyEvent.key_down or keyEvent.keystate is events.KeyEvent.key_hold:
                                if keyEvent.scancode is KEY_ENTER:
                                    #print("Current str: %s" % self.curStr)
                                    self.barcodeReceived.emit(self.curStr)
                                    self.curStr = ""
                                elif keyEvent.scancode in keycodeToASCII:
                                    shift = (self.modifiers[KEY_LEFTSHIFT] or self.modifiers[KEY_RIGHTSHIFT])
                                    self.curStr += keycodeToASCII[keyEvent.scancode][shift]
                                elif keyEvent.scancode in numpadcodeToASCII and self.state[KEY_NUMLOCK]:
                                    str = numpadcodeToASCII[keyEvent.scancode]
            except BlockingIOError:
                # If no events are available, this is thrown
                # No actual error, move on
                pass

        @pyqtSlot()
        def shortcut_activated(self):
            barcode, ok = QInputDialog.getText(self.parent, "Scanner Input", self.shortcutMessage, QLineEdit.Normal, "",
                                               Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

            if ok and barcode:
                self.barcodeReceived.emit(barcode)
elif sys.platform.startswith("win32"):
    class BarcodeScanner(QObject):
        # Signal is emitted once a barcode has been scanned and received
        barcodeReceived = pyqtSignal(str)

        def __init__(self, parent, usbPortNumber, shortcut=None, scannerTitle=None):
            QObject.__init__(self, parent)
            self.parent = parent

            # There is no need to implement the actual barcode reader on Windows since we are using Raspberry Pi 3

            # Set the current string buffer to none
            if shortcut is not None:
                self.shortcut = QShortcut(shortcut, self.parent)
                self.shortcut.activated.connect(self.shortcut_activated)
                if scannerTitle:
                    self.shortcutMessage = "Enter %s barcode: " % scannerTitle
                else:
                    self.shortcutMessage = "Enter barcode: "

        def setPort(self, usbPortNumber):
            # Do nothing
            pass

        def poll(self):
            # Do nothing in poll
            pass

        @pyqtSlot()
        def shortcut_activated(self):
            barcode, ok = QInputDialog.getText(self.parent, "Scanner Input", self.shortcutMessage, QLineEdit.Normal, "",
                                               Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

            if ok and barcode:
                self.barcodeReceived.emit(barcode.strip())