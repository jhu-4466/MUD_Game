# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: tornado server service handler
# Author: m14
# Created: 2023.04.04
# Description: holding the control of tornado server and game server
#              test port：8080
# History:
#    <autohr>    <version>    <time>        <desc>
#    m14         v0.1         2023/04/04    basic build success
# -----------------------------


from utils.helpers.logger_helper import LoggerHelper

import tornado.websocket

import base64
import hashlib


class TornadoMainHandler(tornado.websocket.WebSocketHandler):
    """_summary_
    
    Handles the WebSocket connection.
    
    """
    def __init__(self, application, request, **kwargs):
        self.world = kwargs.pop('world')
        self.tornado_logger = LoggerHelper('tornado')
        
        super().__init__(application, request, **kwargs)
    
    def check_origin(self, origin):
        """_summary_
        
        Override the default method to allow connections from any origin.
        
        """
        self.origin = origin
        version_header = self.request.headers.get('Sec-WebSocket-Version')
        if version_header:
            self.version = int(version_header.split(',')[0])
        return True
    
    def on_connection(self, request):
        """_summary_
        
        Handles the WebSocket connection request.
        
        """
        self.write_message("Welcome to the server!")
        
        # get Headers message by shaking hands.
        headers = request.headers
        key = headers.get('Sec-WebSocket-Key')
        
        # if there is not Sec-WebSocket-Key on headers, return 404
        if not key:
            self.set_status(400)
            self.finish("Invalid WebSocket request")
            return
        
        # build Sec-WebSocket-Accept Headers 
        key = key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        hash = hashlib.sha1(key.encode())
        key = base64.b64encode(hash.digest()).strip().decode('utf-8')
        headers = {
            'Upgrade': 'websocket',
            'Connection': 'Upgrade',
            'Sec-WebSocket-Accept': key,
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
        }

        self.set_status(101)  # it means shaking hands successfully.
        for key, value in headers.items():
            self.set_header(key, value)

    def open(self):
        """_summary_
        
        Handles the WebSocket connection running.
        
        """
        self.tornado_logger.info("someone connects now.")
        self.world.add_session(self)
        
    def on_close(self):
        """_summary_
        
        Handles the WebSocket connection closing.
        
        """
        self.tornado_logger.info("someone quits now.")
        self.world.remove_session(self)
        
    def on_message(self, message):
        """_summary_
        
        Handles the WebSocket message.
        
        """
        self.tornado_logger.info(message)
        self.world.broadcast()

