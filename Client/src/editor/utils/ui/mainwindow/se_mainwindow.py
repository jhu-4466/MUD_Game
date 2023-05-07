# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: se mainwindow ui
# Author: motm14
# Created: 2023.05.06
# Description: se mainwindow ui
# History:
# <autohr>    <version>    <date>        <desc>
# motm14         v0.1    2023/05/    basic build
# -----------------------------


from se_titlebar import SETitleBar
from se_menubar import SEMenuBar

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)
        
        self.setFixedSize(1024, 576)
        
        self.init_ui()
    
    def init_ui(self):
        self.mainlayout = QVBoxLayout(self)
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.mainlayout.setSpacing(0)
        self.mainlayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        # title bar & title menu bar
        self.titlelayout = QVBoxLayout()
        self.titlelayout.setContentsMargins(0, 0, 0, 0)
        self.titlelayout.setSpacing(0)
        self.titlebar = SETitleBar(self)
        self.menubar = SEMenuBar(self)
        self.titlelayout.addWidget(self.titlebar)
        self.titlelayout.addWidget(self.menubar)
        
        self.mainlayout.addLayout(self.titlelayout)
        
        # style
        palette = QPalette()
        palette.setColor(self.backgroundRole(), QColor(255, 255, 255, 128))
        self.setPalette(palette)

    def set_title(self, title):
        self.titlebar.set_title(title)
    
    def set_icon(self, icon):
        self.titlebar.set_icon(icon)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        
        self.titlebar.resize(self.width(), self.titlebar.height())


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.set_title("sky eye")
    window.show()
    app.exec()
