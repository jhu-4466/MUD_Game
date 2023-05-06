# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: editor main window
# Author: motm14
# Created: 2023.04.09
# Description: the game editor including all plugins.
# History:
#    <autohr>    <version>    <time>        <desc>
#    motm14         v0.1         2023/04/09    build the basic
# -----------------------------


from editor.apis.plugins import DockableLocationEnum
from editor.plugins.actor_attributes.plugins import ActorAttributes

from PySide6.QtWidgets import QDockWidget, QApplication, QMainWindow
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCloseEvent, QKeyEvent


class EditorMainWindow(QMainWindow):
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
        
        self.plugins = []
        
        self.init_plugins()
        self.init_ui()
    
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
        self.setWindowTitle("天眼")
        self.setFixedSize(1024, 576)

    def register_plugin(self, plugin):
        """
        
        all plugins register.
        
        """
        widget = plugin.widget
        dock_widget = QDockWidget(plugin.NAME, self)
        dock_widget.setWidget(widget)
        dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.BottomDockWidgetArea)  #  | Qt.TopDockWidgetArea

        if plugin.DOCK_LOCATION == DockableLocationEnum.LEFT:
            self.addDockWidget(Qt.LeftDockWidgetArea, dock_widget)
        elif plugin.DOCK_LOCATION == DockableLocationEnum.RIGHT:
            self.addDockWidget(Qt.RightDockWidgetArea, dock_widget)
        elif plugin.DOCK_LOCATION == DockableLocationEnum.BOTTOM:
            self.addDockWidget(Qt.BottomDockWidgetArea, dock_widget)
        else:
            self.setCentralWidget(widget)

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