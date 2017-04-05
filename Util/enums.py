from enum import *


class ScrollingType(IntEnum):
    NoOvershoot = 1
    LeftClick = 2
    RightClick = 4
    QuickAcceleration = 8

    Default = NoOvershoot | LeftClick
    SpinBox = NoOvershoot | LeftClick | QuickAcceleration

class WindowType(IntEnum):
    Main = 0
    Favorites = 1
    PurchaseHistory = 2
    Settings = 3

class KeyboardState(IntEnum):
    Normal = 0
    Shift = 1
    Caps = 2
