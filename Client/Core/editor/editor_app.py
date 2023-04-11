# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: editor main window
# Author: k14
# Created: 2023.04.09
# Description: the game editor including all plugins.
# History:
#    <autohr>    <version>    <time>        <desc>
#    k14         v0.1         2023/04/09    build the basic
# -----------------------------


from core.editor.apis.plugins import DockableLocationEnum

from PyQt5.QtWidgets import QDockWidget, QMainWindow
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCloseEvent


class EditorMainWindow(QMainWindow):
    """_summary_
    
    Editor main window.
    
    Attributes:
        plugins: all plugin widgets.
    
    Signal:
        signal_close: close the main window.
    """
    signal_close = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        self.plugins = []
        
        self.init_ui()
    
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

        widget.show()

    def closeEvent(self, event: QCloseEvent):
        """_summary_
        
        rewrite closing main window.
        
        """
        self.signal_close.emit()
        event.ignore()