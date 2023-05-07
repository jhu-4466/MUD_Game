# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: se mainwindow menubar and menubar buttons ui
# Author: motm14
# Created: 2023.05.07
# Description: se mainwindow menubar and menubar buttons ui
# History:
# <autohr>    <version>    <date>        <desc>
# motm14         v0.1    2023/05/07    basic build
# -----------------------------


from PySide6.QtWidgets import QMenu, QMenuBar, QHBoxLayout
from PySide6.QtGui import QPainter, QAction
from PySide6.QtCore import Qt


class SEMenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.menus = {}
        self.setFixedHeight(24)
        
        self.init_ui()
    
    def init_ui(self):
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        # style
        self.setStyleSheet("""
            QMenuBar {
                background: rgba(255, 255, 255, 128);
                border: none;
                font-weight: bold;
                font-size: 13px;
                color: #444444;
                spacing: 0px;
            }
            QMenu {
                background: white;
                border: none;
                font-weight: bold;
                font-size: 13px;
                color: #444444;
            }
            QMenu::item {
                background: white;
                color: #444444;
                padding: 8px 20px;
            }
            QMenu::item:selected {
                background: rgb(156, 156, 156);
            }
            QLabel {
                background: transparent;
                border: none;
            }
        """)

    def paintEvent(self, event):
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.drawLine(self.rect().topLeft(), self.rect().topRight())
        
    def add_menu(self, menu_name):
        """
        
        add a menu in the menu bar.

        Args:
            menu_name (str): menu name
        """        
        menu = QMenu(menu_name, self)
        menu.addSeparator()

        self.addMenu(menu)
        self.menus[menu_name] = menu
    
    def add_menu_action(self, menu_name, action_name, action_func):
        """
        
        add a menu action in the menu.

        Args:
            menu_name (str): menu name
            action_name (str): action name
            action_func (function): action triggered connect function
        """      
        menu = self.menus[menu_name]
        action = QAction(action_name, menu)
        action.triggered.connect(action_func)
        
        menu.addAction(action)