from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from enum import Enum
from Util.enums import *

def setupScrolling(obj, scrollingType=None):
    scroller = QScroller.scroller(obj)
    scroller.grabGesture(obj, QScroller.LeftMouseButtonGesture)

    # Setup the scrolling properties based on the scrollingType
    scrollerProps = scroller.scrollerProperties()
    if scrollingType == ScrollingType.Default or scrollingType == None:
        scrollerProps.setScrollMetric(QScrollerProperties.HorizontalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
        scrollerProps.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
        scrollerProps.setScrollMetric(QScrollerProperties.OvershootScrollDistanceFactor, 0)
        scrollerProps.setScrollMetric(QScrollerProperties.OvershootDragDistanceFactor, 0)
    elif scrollingType == ScrollingType.SpinBox:
        scroller.grabGesture(obj, QScroller.RightMouseButtonGesture)

        scrollerProps.setScrollMetric(QScrollerProperties.HorizontalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
        scrollerProps.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
        scrollerProps.setScrollMetric(QScrollerProperties.OvershootScrollDistanceFactor, 0)
        scrollerProps.setScrollMetric(QScrollerProperties.OvershootDragDistanceFactor, 0)
        scrollerProps.setScrollMetric(QScrollerProperties.ScrollingCurve, QEasingCurve(QEasingCurve.OutExpo))
        scrollerProps.setScrollMetric(QScrollerProperties.DecelerationFactor, 0.01)
        scrollerProps.setScrollMetric(QScrollerProperties.AcceleratingFlickSpeedupFactor, 6)

    scroller.setScrollerProperties(scrollerProps)
