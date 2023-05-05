# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: se main window ui
# Author: motm14
# Created: 2023.05.05
# Description: se main window ui
# History:
#    <autohr>    <version>    <time>        <desc>
#    motm14         v0.1    2023/05/05    basic build
# -----------------------------


from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent


class FramelessWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        # 设置窗口属性
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 设置背景色和样式
        self.setStyleSheet("background-color: rgba(128, 128, 128, 128); border: 1px solid gray;")

        # 初始化窗口大小和位置
        self.resize(400, 300)
        self.move(100, 100)

    def resizeEvent(self, e):
        super().resizeEvent(e)


if __name__ == "__main__":
    app = QApplication([])
    window = FramelessWindow()
    window.show()
    app.exec()