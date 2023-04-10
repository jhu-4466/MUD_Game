# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: connect server end with tornado
# Author: k14
# Created: 2023.04.04
# Description: holding the control of tornado server and game server
#              test port：8080
# History:
#    <autohr>    <version>    <time>        <desc>
#    k14         v0.1         2023/04/04    basic build success
# -----------------------------

import tornado.web
import tornado.websocket
import tornado.ioloop

import base64
import hashlib
import logging
import datetime


class Game_Server:
    """_summary_
    
    it tackles the core logics about game server.
    
    Attributes:
        clients_list: all client connected the game server.
    """
    def __init__(self):
        self.clients_list = set()
    
    def add_client(self, client):
        """_summary_
        
        Add the client into the game server.

        Attributes:
            client: Tornado_Client_App
        """
        self.clients_list.add(client)
    
    def remove_client(self, client):
        """_summary_
        
        Remove the client into the game server.
        
        Attributes:
            client: Tornado_Client_App
        """
        self.clients_list.remove(client)
    
    def broadcast(self, message="Hello! My consumer."):
        """_summary_
        
        a connect test.
        
        Attributes:
            message: send message to client.
        """
        for client in self.clients_list:
            client.write_message(message)


class Tornado_Main_Handler(tornado.websocket.WebSocketHandler):
    """_summary_
    
    Handles the WebSocket connection.
    
    """
    def __init__(self, application, request, **kwargs):
        self.game_server = kwargs.pop('game_server')
        
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
        logging.info("someone connects now.")
        self.game_server.add_client(self)
        
    def on_close(self):
        """_summary_
        
        Handles the WebSocket connection closing.
        
        """
        logging.info("someone quits now.")
        self.game_server.remove_client(self)
        
    def on_message(self, message):
        """_summary_
        
        Handles the WebSocket message.
        
        """
        logging.info(message)
        self.game_server.broadcast()


class Tornado_Server_App:
    """_summary_
    
    it controls the tornado server end.
    
    Attributes:
        game_server: it includes the core logics of the games
        _app: it is a real example about web app
    """
    def __init__(self, game_server: Game_Server):
        self.game_server = game_server
        self._app = tornado.web.Application([
            (r"/websocket", Tornado_Main_Handler, dict(game_server=self.game_server)),  # the application has the only rout rule of websocket
        ],
        template_path="templates", static_path="static",  # specify the folder path about template, static
        websocket_compression_options = {},  # Prohibit the compression
        )

    def start(self, port: int=8080):
        """_summary_

        reload the function named start to start the tornado.
        
        Args:
            port (int): the port for server.
        """
        self._app.listen(port=port)
        tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    test_game_server_app = Game_Server()
    test_server_app = Tornado_Server_App(test_game_server_app)
    
    try:
        test_server_app.start()
    except KeyboardInterrupt:
        import sys
        sys.exit()