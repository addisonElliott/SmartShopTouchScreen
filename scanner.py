from exception import *
from evdev import *
import re

class BarcodeScanner:
    def __init__(self, usbPortNumber):
        self.modifiers = {
            ecodes.KEY_LEFT0,  # Right GUI - (usually the Windows key)
            0,  # Right ALT
            ecodes.KEY_RIGHTSHIFT: 0,  # Right Shift
            ecodes.KEY_RIGHTCTRL: 0,  # Right Control
            0,  # Left GUI - (again, usually the Windows key)
            0,  # Left ALT
            ecodes.KEY_LEFTSHIFT: 0,  # Left Shift
            0  # Left Control
        }
        self.state = {
            ecodes.LED_CAPSL:   0, # Caps Lock
            ecodes.LED_NUML:    0, # Num Lock
            ecodes.LED_SCROLLL: 0  # Scroll Lock
        }

        rePhysicalLoc = re.compile("usb\-.*\..*\-1\.%i.*" % usbPortNumber)

        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        self.device = None
        for device in devices:
            if rePhysicalLoc.match(device.phys) is not None:
                self.device = device
                break

        # If unable to find the device at port number, raise error
        if self.device is None:
            raise SmartShopException("Unable to find input device located at port %i" % usbPortNumber)

        ledStates = self.device.leds()
        for led in ledStates:
            self.state[led] = 1

    def poll(self):
        try
            # Read all of the events from the loop
            events = self.device.read()

            for event in events:
                if event.type is evdev.ecodes.EV_KEY:
                    keyEvent = evdev.util.categorize(event)
                    if keyEvent.keystate is evdev.events.KeyEvent.key_down or \
                        keyEvent.keystate is evdev.events.KeyEvent.key_hold:
                        i = 4
        except BlockingIOError:
            # If no events are available, this is thrown
            # No actual error, move on
            pass