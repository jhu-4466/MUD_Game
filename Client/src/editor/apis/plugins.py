# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: base plugin class
# Author: yang chaohuan
# Created: 2023.04.10
# Description: the base class about plugin
# History:
#    <author>    <version>    <time>        <desc>
#    m14         v0.1         2023/04/10    build the basic
# -----------------------------


from editor.apis.widgets import PluginMainWidget

from PySide6.QtCore import QObject


class PluginBase(QObject):
    """
    
    base plugin.
    
    Args:
        parent: parent widget
    """
    NAME = None
    ORDER = 0

    def __init__(self, parent):
        super().__init__()
        self.main = parent

    def initialize(self):
        self.on_initialize()

    def on_initialize(self):
        pass

    def on_all_plugins_initialize(self):
        pass

    def close(self):
        self.on_close()

    def on_close(self):
        pass


class DockableLocationEnum:
    CENTER = 0
    LEFT = 1
    RIGHT = 2
    BOTTOM = 3


class DockablePluginBase(PluginBase):
    """
    
    base plugin.
    
    Args:
        parent: parent widget
        WIDGET_CLASS: plugin widget
        DOCK_LOCATION: plugin index in the main window
    """
    WIDGET_CLASS = PluginMainWidget
    DOCK_LOCATION = DockableLocationEnum.CENTER

    def __init__(self, parent):
        super().__init__(parent)

    def initialize(self):
        self.widget = self.WIDGET_CLASS(self.NAME, self)
        self.on_initialize()

    def get_title(self):
        return self.NAME