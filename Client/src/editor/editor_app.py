# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: editor main window
# Author: m14
# Created: 2023.04.09
# Description: the game editor including all plugins.
# History:
#    <author>    <version>    <time>        <desc>
#    m14         v0.1         2023/04/09    build the basic
# -----------------------------


from editor.apis.plugins import DockableLocationEnum
from editor.plugins.actor_attributes.plugins import ActorAttributes

from editor.utils.ui.mainwindow import SEMainWindow
from editor.utils.ui.tabwidget import SETabWidget

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCloseEvent, QKeyEvent


class EditorMainWindow(SEMainWindow):
    """
    
    Editor main window.
    
    Args:
        plugins: all plugin widgets.
    
    Signal:
        signal_close: close the main window.
    """
    signal_close = Signal()
    
    def __init__(self):
        super().__init__()
        
        self.init_ui()
        self.init_plugins()
    
    def init_plugins(self):
        """
        
        init main window plugins and attributes.
        
        """
        # Register widget plugins
        self.actor_attributes_plugin = ActorAttributes(self)
        self.actor_attributes_plugin.initialize()
        
        self.plugins = [self.actor_attributes_plugin]
        
        for plugin in self.plugins:
            self.register_plugin(plugin)
    
    def init_ui(self):
        """
        
        init main window ui.
        
        """
        self.set_title("天眼")
        self.setFixedSize(1366, 768)
        
        self.left_widgets = SETabWidget(self)
        self.central_widgets = SETabWidget(self)
        self.right_widgets = SETabWidget(self)
        self.widgets_layout.addWidget(self.left_widgets, 5)
        self.widgets_layout.addWidget(self.central_widgets, 9)
        self.widgets_layout.addWidget(self.right_widgets, 4)
        
        self.widgets_layout

    def register_plugin(self, plugin):
        """
        
        all plugins register.
        
        """
        if plugin.DOCK_LOCATION == DockableLocationEnum.LEFT:
            self.left_widgets.addTab(plugin.widget, plugin.NAME)
        elif plugin.DOCK_LOCATION == DockableLocationEnum.RIGHT:
            self.right_widgets.addTab(plugin.widget, plugin.NAME)
        else:
            self.central_widgets.addTab(plugin.widget, plugin.NAME)

    def closeEvent(self, event: QCloseEvent):
        """
        
        rewrite closing main window.
        
        """
        self.signal_close.emit()
        event.ignore()
    
    def keyPressEvent(self, event: QKeyEvent):
        """
        
        rewrite key press event in the main window.
        
        """
        if event.key() == Qt.Key.Key_C and \
            QApplication.keyboardModifiers() == Qt.KeyboardModifier.ControlModifier:
            self.signal_close.emit()