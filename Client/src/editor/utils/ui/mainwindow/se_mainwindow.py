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

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)
        
        self.setFixedSize(1024, 576)
        
        self.init_ui()
    
    def init_ui(self):
        self.titlebar = SETitleBar(self)
        self.titlebar.raise_()

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
