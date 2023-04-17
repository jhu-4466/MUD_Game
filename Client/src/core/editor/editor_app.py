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


from core.editor.apis.plugins import DockableLocationEnum

from PyQt5.QtWidgets import QDockWidget, QMainWindow, QApplication
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCloseEvent, QKeyEvent


class EditorMainWindow(QMainWindow):
    """_summary_
    
    Editor main window.
    
    Args:
        plugins: all plugin widgets.
    
    Signal:
        signal_close: close the main window.
    """
    signal_close = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        self.init_plugins()
        self.init_ui()
    
    def init_plugins(self):
        """_summary_
        
        init main window plugins and attributes.
        
        """
        self.plugins = []
    
    def init_ui(self):
        """_summary_
        
        init main window ui.
        
        """
        self.setFixedSize(1024, 768)

    def register_plugin(self, plugin):
        """_summary_
        
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
        """_summary_
        
        rewrite closing main window.
        
        """
        self.signal_close.emit()
        event.ignore()
        
    def keyPressEvent(self, event: QKeyEvent):
        """_summary_
        
        rewrite key press event in the main window.
        
        """
        if event.key() == Qt.Key.Key_C and \
            QApplication.keyboardModifiers() == Qt.KeyboardModifier.ControlModifier:
            self.signal_close.emit()