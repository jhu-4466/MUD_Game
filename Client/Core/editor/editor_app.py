# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: client main app
# Author: k14
# Created: 2023.04.09
# Description: the game editor including all plugins.
# History:
#    <autohr>    <version>    <time>        <desc>
#    k14         v0.1         2023/04/09    build the basic
# -----------------------------


from PyQt5.QtWidgets import QWidget, QMainWindow  #, QApplication
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCloseEvent

import sys


class Editor_Main_Window(QMainWindow):
    close_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()

    def closeEvent(self, event: QCloseEvent):
        self.close_signal.emit()
        event.ignore()


# if __name__ == '__main__':
#     editor_app = QApplication([])
#     editor_main_window = Editor_Main_Window()
#     editor_main_window.show()
    
#     sys.exit(editor_app.exec_())