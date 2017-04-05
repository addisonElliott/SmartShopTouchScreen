from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from enum import Enum
from Util.enums import *

def setupScrolling(obj, scrollingType=ScrollingType.Default):
    scroller = QScroller.scroller(obj)
    scrollerProps = scroller.scrollerProperties()

    if scrollingType & ScrollingType.LeftClick:
        scroller.grabGesture(obj, QScroller.LeftMouseButtonGesture)

    if scrollingType & ScrollingType.RightClick:
        scroller.grabGesture(obj, QScroller.RightMouseButtonGesture)

    if scrollingType & ScrollingType.NoOvershoot:
        scrollerProps.setScrollMetric(QScrollerProperties.HorizontalOvershootPolicy,
                                      QScrollerProperties.OvershootAlwaysOff)
        scrollerProps.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy,
                                      QScrollerProperties.OvershootAlwaysOff)
        scrollerProps.setScrollMetric(QScrollerProperties.OvershootScrollDistanceFactor, 0)
        scrollerProps.setScrollMetric(QScrollerProperties.OvershootDragDistanceFactor, 0)

    if scrollingType & ScrollingType.QuickAcceleration:
        scrollerProps.setScrollMetric(QScrollerProperties.ScrollingCurve, QEasingCurve(QEasingCurve.OutExpo))
        scrollerProps.setScrollMetric(QScrollerProperties.DecelerationFactor, 0.01)
        scrollerProps.setScrollMetric(QScrollerProperties.AcceleratingFlickSpeedupFactor, 6)

    scroller.setScrollerProperties(scrollerProps)
