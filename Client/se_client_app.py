# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: client main app
# Author: motm14
# Created: 2023.04.09
# Description: the main client including interface and communication.
# History:
#    <autohr>    <version>    <time>        <desc>
#    motm14         v0.1         2023/04/09    build the basic
# -----------------------------


from core.services.tornado_service_client import TornadoServiceClient, TornadoThread

from core.editor.editor_app import EditorMainWindow
from core.editor.plugins.actor_attributes.plugins import ActorAttributes

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, QEventLoop, QCoreApplication

import sys
import threading


class SEClientApp:
    """_summary_
    
    As a client, combining pyqt and tornado.
    
    Attributes:
        editor_app_communication_client: tornado client
        editor_app_communication_thread: tornado thread
        editor_app: editor app, it must run in the main thread
        editor_app_main_window: editor main window
    """
    def __init__(self, url: str):
        self.editor_app_communication_client = TornadoServiceClient(url)
        self.editor_app_communication_thread = TornadoThread(
            self.editor_app_communication_client)
        
        self.editor_app = QApplication([])
        self.editor_app.setQuitOnLastWindowClosed(True)
        self.editor_app_main_window = EditorMainWindow()
        self.editor_app_main_window.signal_close.connect(self.close)
        
        # Register widget plugins
        actor_attributes_plugin = ActorAttributes(self.editor_app_main_window)
        actor_attributes_plugin.initialize()
        self.editor_app_main_window.plugins = [actor_attributes_plugin]
        
        for plugin in self.editor_app_main_window.plugins:
            self.editor_app_main_window.register_plugin(plugin)
        
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
        self.editor_app_communication_client.on_close()
        
        self.editor_app_main_window.close()

        sys.exit()


if __name__ == "__main__":
    url = "ws://127.0.0.1:8080/websocket"
    client = SEClientApp(url)
    
    try:
        client.start()
    except KeyboardInterrupt:
        client.close()