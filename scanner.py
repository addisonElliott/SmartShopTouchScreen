from exception import *
from evdev import *
from ecodes import *
import re

keycodeToASCII = {
    # Scancode: ASCIICode
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

class BarcodeScanner:
    def __init__(self, usbPortNumber):
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
            LED_CAPSL:   0, # Caps Lock
            LED_NUML:    0, # Num Lock
            LED_SCROLLL: 0  # Scroll Lock
        }

        rePhysicalLoc = re.compile("usb\-.*\..*\-1\.%i.*" % usbPortNumber)

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
        for led in ledStates:
            self.state[led] = 1

    def poll(self):
        try:
            # Read all of the events from the loop
            events = self.device.read()

            for event in events:
                if event.type is EV_KEY:
                    keyEvent = util.categorize(event)

                    if keyEvent.keycode in self.modifiers:
                        if keyEvent.keystate is events.KeyEvent.key_down:
                            self.modifiers[keyEvent.keycode] = 1
                        elif keyEvent.keystate is events.KeyEvent.key_up:
                            self.modifiers[keyEvent.keycode] = 0
                    elif keyEvent.keycode in self.state:
                        if keyEvent.keystate is events.KeyEvent.key_down:
                            self.state[keyEvent.keycode] = 1
                        elif keyEvent.keystate is events.KeyEvent.key_up:
                            self.state[keyEvent.keycode] = 0
                    elif keyEvent.keystate is events.KeyEvent.key_down or \
                        keyEvent.keystate is events.KeyEvent.key_hold:
                        if keyEvent.keycode in keycodeToASCII:
                            shift = (self.modifiers[KEY_LEFTSHIFT] or self.modifiers[KEY_RIGHTSHIFT])
                            str = keycodeToASCII[keyEvent.keycode][shift]
                        elif keyEvent.keycode in numpadcodeToASCII:
                            str = numpadcodeToASCII[keyEvent.keycode]
        except BlockingIOError:
            # If no events are available, this is thrown
            # No actual error, move on
            pass