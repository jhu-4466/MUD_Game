# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: base widget class
# Author: yang chaohuan
# Created: 2023.04.10
# Description: the base class about widget
# History:
#    <author>    <version>    <time>        <desc>
#    m14         v0.1         2023/04/10    build the basic
# -----------------------------


from PySide6.QtWidgets import QWidget


class PluginMainWidget(QWidget):
    """
    
    base widget.
    
    Args:
        parent: parent widget
        WIDGET_CLASS: plugin widget
        DOCK_LOCATION: plugin index in the main window
    """
    def __init__(self, name, plugin, parent=None):
        super().__init__(parent=parent)
        
        self._name = name
        self._plugin = plugin
        self._parent = parent