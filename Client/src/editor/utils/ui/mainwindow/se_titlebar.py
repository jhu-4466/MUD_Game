# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: se mainwindow titlebar and titlebar buttons ui
# Author: motm14
# Created: 2023.05.06
# Description: se mainwindow titlebar and titlebar buttons ui
# History:
# <autohr>    <version>    <date>        <desc>
# motm14         v0.1    2023/05/06    basic build
# -----------------------------


from PySide6.QtCore import Qt, QPointF, QSize, QEvent
from PySide6.QtGui import QColor, QPainter, QIcon, QPen, QPainterPath
from PySide6.QtWidgets import QAbstractButton, QHBoxLayout, QLabel, QWidget

from enum import Enum
import sys
import win32api
import win32gui
import win32con


class SETitleBarButtonState(Enum):
    NORMAL = 0
    HOVER = 1
    PRESSED = 2


class SETitleBarButton(QAbstractButton):
    """
    
    SE titlebar base button

    Attributes:
        ____state____ (SETitleBarButtonState): button state
        ____normal_color____ (QColor): icon normal color
        ____hover_color____ (QColor): icon hover color 
        ____pressed_color____ (QColor): icon press color
        ____normal_bg_color____ (QColor): backgournd normal color
        ____hover_bg_color____ (QColor): backgournd hover color 
        ____pressed_bg_color____ (QColor): backgournd press color 
    """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        self.setCursor(Qt.ArrowCursor)
        self.setFixedSize(46, 32)
        
        self.____state____ = SETitleBarButtonState.NORMAL

        # icon color
        self.____normal_color____ = QColor(128, 128, 128)
        self.____hover_color____ = QColor(100, 100, 100)
        self.____pressed_color____ = QColor(156, 156, 156)

        # background color
        self.____normal_bg_color____ = QColor(64, 64, 64)
        self.____hover_bg_color____ = QColor(100, 100, 100, 26)
        self.____pressed_bg_color____ = QColor(156, 156, 156, 51)

    def setState(self, state):
        """ 
        
        set the state of button

        Args:
            state (SETitleBarButtonState): the state of button
        """
        self.____state____ = state
        
        self.update()

    def isPressed(self):
        return self.____state____ == SETitleBarButtonState.PRESSED

    @property
    def normal_color(self):
        return self.____normal_color____
    
    @property
    def hover_color(self):
        return self.____hover_color____

    @property
    def pressed_color(self):
        return self.____pressed_color____

    @property
    def normal_bg_color(self):
        return self.____normal_bg_color____

    @property
    def hover_bg_color(self):
        return self.____hover_bg_color____

    @property
    def pressed_bg_color(self):
        return self.____pressed_bg_color____

    def set_normal_color(self, color):
        """ 
        
        set the icon color of the button in normal state

        Args:
            color (QColor): icon color
        """
        self.____normal_color____ = QColor(color)
        
        self.update()

    def set_hover_color(self, color):
        """ 
        
        set the icon color of the button in hover state

        Args:
            color (QColor): icon color
        """
        self.____hover_color____ = QColor(color)
        
        self.update()

    def set_pressed_color(self, color):
        """ 
        
        set the icon color of the button in pressed state

        Args:
            color (QColor): icon color
        """
        self.____pressed_color____ = QColor(color)
        
        self.update()

    def set_normal_bg_color(self, color):
        """ 
        
        set the background color of the button in normal state

        Args:
            color (QColor): background color
        """
        self.____normal_bg_color____ = QColor(color)
        
        self.update()

    def set_hover_bg_color(self, color):
        """ 
        
        set the background color of the button in hover state

        Args:
            color (QColor): background color
        """
        self.____hover_bg_color____ = QColor(color)
        
        self.update()

    def set_pressed_bg_color(self, color):
        """ 
        
        set the background color of the button in pressed state

        Args:
            color (QColor): background color
        """
        self.____pressed_bg_color____ = QColor(color)
        
        self.update()

    def enterEvent(self, event):
        """
        
        auto trigger when mouse goes into the area of button.

        """
        self.setState(SETitleBarButtonState.HOVER)
        
        super().enterEvent(event)

    def leaveEvent(self, event):
        """
        
        auto trigger when mouse leaves from the area of button.

        """
        self.setState(SETitleBarButtonState.NORMAL)
        
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        self.setState(SETitleBarButtonState.PRESSED)
        
        super().mousePressEvent(event)

    def _get_colors(self):
        """ get the icon color and background color """
        if self.____state____ == SETitleBarButtonState.NORMAL:
            return self.____normal_color____, self.____normal_bg_color____
        elif self.____state____ == SETitleBarButtonState.HOVER:
            return self.____hover_color____, self.____hover_bg_color____

        return self.____pressed_color____, self.____pressed_bg_color____


class SEMinimizeButton(SETitleBarButton):
    """ 
    
    Minimize button 
    
    """
    def paintEvent(self, e):
        painter = QPainter(self)
        color, bg_color = self._get_colors()

        # draw background
        painter.setBrush(bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        painter.setBrush(Qt.NoBrush)
        pen = QPen(color, 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(18, 16, 28, 16)


class SEMaximizeButton(SETitleBarButton):
    """ 
    Maximize button 
    
    Attributes:
        _is_max (bool): whether the widget is max now.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._is_max = False

    def setMaxState(self, is_max: bool):
        """ update the maximized state and icon """
        if self._is_max == is_max:
            return
        self._is_max = is_max
        
        self.setState(SETitleBarButtonState.NORMAL)

    def paintEvent(self, event):
        painter = QPainter(self)
        color, bg_color = self._get_colors()

        # draw background
        painter.setBrush(bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        painter.setBrush(Qt.NoBrush)
        pen = QPen(color, 1)
        pen.setCosmetic(True)
        painter.setPen(pen)

        r = self.devicePixelRatioF()
        painter.scale(1/r, 1/r)
        if not self._is_max:
            painter.drawRect(int(18*r), int(11*r), int(10*r), int(10*r))
        else:
            painter.drawRect(int(18*r), int(13*r), int(8*r), int(8*r))
            x0 = int(18*r)+int(2*r)
            y0 = 13*r
            dw = int(2*r)
            path = QPainterPath(QPointF(x0, y0))
            path.lineTo(x0, y0-dw)
            path.lineTo(x0+8*r, y0-dw)
            path.lineTo(x0+8*r, y0-dw+8*r)
            path.lineTo(x0+8*r-dw, y0-dw+8*r)
            painter.drawPath(path)


class SECloseButton(SETitleBarButton):
    """ 
    
    Close button

    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.set_hover_bg_color(QColor(255, 0, 0))
    
    def paintEvent(self, event):
        painter = QPainter(self)
        color, bg_color = self._get_colors()

        # draw background
        painter.setBrush(bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        painter.setBrush(Qt.NoBrush)
        pen = QPen(color, 1.41)
        pen.setCosmetic(True)
        painter.setPen(pen)

        # cacluate the center pos
        center = self.rect().center()
        r = self.devicePixelRatioF()
        painter.scale(1 / r, 1 / r)
        icon_size = QSize(7 * r, 7 * r)
        icon_pos = QPointF(center.x() - icon_size.width() / 2, center.y() - icon_size.height() / 2)

        path = QPainterPath()
        path.moveTo(icon_pos + QPointF(0, 0))
        path.lineTo(icon_pos + QPointF(7 * r, 7 * r))
        path.moveTo(icon_pos + QPointF(0, 7 * r))
        path.lineTo(icon_pos + QPointF(7 * r, 0))
        painter.drawPath(path)


class SETitleBar(QWidget):
    """ Title bar """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.min_button = SEMinimizeButton(parent=self)
        self.close_button = SECloseButton(parent=self)
        self.max_button = SEMaximizeButton(parent=self)
        
        self.icon_label = QLabel(self)
        self.icon_label.setFixedSize(25, 25)
        # add title label
        self.titleLabel = QLabel(self)
        self.titleLabel.setStyleSheet("""
            QLabel {
                background: transparent;
                font: 13px 'Segoe UI';
                padding: 0 4px
            }
        """)
        
        self.hBoxLayout = QHBoxLayout(self)
        
        self.____is_double_click_enabled____ = True

        self.setFixedHeight(32)

        # add buttons to layout
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.min_button, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.max_button, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.close_button, 0, Qt.AlignRight)

        self.hBoxLayout.insertSpacing(0, 10)
        self.hBoxLayout.insertWidget(1, self.icon_label, 0, Qt.AlignLeft)
        self.hBoxLayout.insertWidget(2, self.titleLabel, 0, Qt.AlignLeft)

        # connect signal to slot
        self.min_button.clicked.connect(self.window().showMinimized)
        self.max_button.clicked.connect(self._toggle_max_state)
        self.close_button.clicked.connect(self.window().close)

        self.window().windowIconChanged.connect(self.set_icon)
        self.window().windowTitleChanged.connect(self.set_title)
        self.window().installEventFilter(self)
    
    @property
    def is_double_click_enabled(self):
        return self.____is_double_click_enabled____
    
    def set_double_click_enbaled(self, value):
        self.____is_double_click_enabled____ = value
    
    def set_icon(self, icon):
        """ 
        
        set the title of title bar

        Args:
            icon (QIcon | QPixmap | str): the icon of title bar
        """
        self.icon_label.setPixmap(QIcon(icon).pixmap(20, 20))
    
    def set_title(self, title):
        """ 
        
        set the title of title bar

        Args:
            title (str): the title of title bar
        """
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()    

    def _toggle_max_state(self):
        """ 
        
        Toggles the maximization state of the window and change icon
        
        """
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def eventFilter(self, obj, event):
        """
        
        filter events, just handle window statechange event
        
        """
        if obj is self.window():
            if event.type() == QEvent.WindowStateChange:
                self.max_button.setMaxState(self.window().isMaximized())
                return False

        return super().eventFilter(obj, event)

    def mouseDoubleClickEvent(self, event):
        """ 
        
        Toggles the maximization state of the window 
        
        """
        if event.button() != Qt.LeftButton or not self.____is_double_click_enabled____:
            return

        self._toggle_max_state()

    def _is_drag_region(self, pos):
        """ 
        
        Check whether the position belongs to the area where dragging is allowed 
        
        """
        width = 0
        for button in self.findChildren(SETitleBarButton):
            if button.isVisible():
                width += button.width()

        return 0 < pos.x() < self.width() - width

    def _has_button_pressed(self):
        """ 
        
        whether any button is pressed
        
        """
        return any(btn.isPressed() for btn in self.findChildren(SETitleBarButton))

    def can_drag(self, pos):
        """ 
        
        whether the position is draggable
        
        """
        return self._is_drag_region(pos) and not self._has_button_pressed()

    def mouseMoveEvent(self, event):
        if sys.platform != "win32" or not self.can_drag(event.pos()):
            return

        win32gui.ReleaseCapture()
        win32api.SendMessage(
            int(self.window().winId()),
            win32con.WM_SYSCOMMAND,
            win32con.SC_MOVE | win32con.HTCAPTION,
            0
        )

    def mousePressEvent(self, event):
        if sys.platform != "win32" or not self.can_drag(event.pos()):
            return

        pass