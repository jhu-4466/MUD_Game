# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: client main app
# Author: k14
# Created: 2023.04.09
# Description: the main client including interface and communication.
# History:
#    <autohr>    <version>    <time>        <desc>
#    k14         v0.1         2023/04/09    build the basic
# -----------------------------


from core.editor.editor_app import Editor_Main_Window
from core.routes.connect_client_app import Tornado_Client_App, Tornado_Thread

from PyQt5.QtWidgets import QApplication

import sys


class SE_Client_App:
    """_summary_
    
    As a client, combining pyqt and tornado.
    
    Attributes:
        editor_app_communication_client: tornado client
        editor_app_communication_thread: tornado thread
        editor_app: editor app, it must run in the main thread
        editor_app_main_window: editor main window
    """
    def __init__(self, url: str):
        self.editor_app_communication_client = Tornado_Client_App(url)
        self.editor_app_communication_thread = Tornado_Thread(
            self.editor_app_communication_client)
        
        self.editor_app = QApplication([])
        self.editor_app.setQuitOnLastWindowClosed(True)
        self.editor_app_main_window = Editor_Main_Window()
        self.editor_app_main_window.close_signal.connect(self.close)
        
    def start(self):
        """_summary_
        
        Runs SE_Client_App.

        """
        self.editor_app_main_window.show()
        self.editor_app_communication_thread.start()
        
        self.editor_app.exec_()
    
    def close(self):
        """_summary_
        
        Close SE_Client_App.

        """
        self.editor_app_communication_client.close()
        self.editor_app_main_window.close()
        
        sys.exit()


if __name__ == "__main__":
    url = "ws://127.0.0.1:8080/websocket"
    client = SE_Client_App(url)
    
    try:
        client.start()
    except KeyboardInterrupt:
        client.close()