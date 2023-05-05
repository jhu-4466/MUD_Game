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

from PySide6.QtWidgets import QDockWidget, QApplication
from PySide6.QtCore import Qt, Signal, QFile
from PySide6.QtGui import QCloseEvent, QKeyEvent


class EditorMainWindow(QWidget):
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
        
        self.init_plugins()
        self.init_ui()
    
    def init_plugins(self):
        """
        
        init main window plugins and attributes.
        
        """
        self.plugins = []
    
    def init_ui(self):
        """
        
        init main window ui.
        
        """
        style_file = QFile('../resources/ui/mainwindow/mainwindow.qss')
        style_file.open(QFile.ReadOnly | QFile.Text)
        style = style_file.readAll()
        style = bytes(style).decode('utf-8')
        self.setStyleSheet(style)
        
        self.setWindowTitle("天眼")
        self.setFixedSize(1024, 768)

    def register_plugin(self, plugin):
        """
        
        all plugins register.
        
        """
        return
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