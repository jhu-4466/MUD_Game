# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: actor information widget
# Author: m14
# Created: 2023.04.10
# Description: actor information widget
# History:
#    <author>    <version>    <time>        <desc>
#    m14         v0.1         2023/04/10    build the basic
# -----------------------------


from core.editor.apis.widgets import PluginMainWidget

from PySide6.QtWidgets import QVBoxLayout, QWidget


class ActorAttributesWidget(PluginMainWidget):
    def __init__(self, name, plugin, parent=None):
        super().__init__(name, plugin, parent)
        
        self.setup()
    
    def setup(self):
        self.init_plugins()
        self.init_ui()
    
    def init_plugins(self):
        pass
    
    def init_ui(self):
        vlayout = QVBoxLayout()
        
        vlayout.addWidget(QWidget())
        
        self.setLayout(vlayout)