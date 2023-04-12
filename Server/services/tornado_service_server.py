# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: connect server end with tornado
# Author: m14
# Created: 2023.04.04
# Description: holding the control of tornado server and game server
#              test port：8080
# History:
#    <autohr>    <version>    <time>        <desc>
#    m14         v0.1         2023/04/04    basic build success
#    m14         v1.0         2023/04/11    run in an other thread
# -----------------------------


from .tornado_service_handler import TornadoMainHandler

import tornado.web
import tornado.websocket
import tornado.ioloop

import threading


class TornadoServiceServer:
    """_summary_
    
    it controls the tornado server end.
    
    Attributes:
        game_server: it includes the core logics of the games
        ____app____: it is a real example about web app
    """
    def __init__(self, world, logger):
        self.world = world
        self.logger = logger
        
        self.initialize()
    
    def initialize(self):
        self.____app____ = tornado.web.Application([(r"/websocket", TornadoMainHandler, 
                                              dict(world=self.world, logger=self.logger)),  # the application has the only rout rule of websocket
                                            ],
                                            template_path="templates", static_path="static",  # specify the folder path about template, static
                                            websocket_compression_options = {},  # Prohibit the compression
                                            )
        self.____io_loop____ = tornado.ioloop.IOLoop()

    def on_start(self, port: int=8080):
        """_summary_

        reload the function named start to start the tornado.
        
        Args:
            port (int): the port for server.
        """
        self.____io_loop____.make_current()
        
        self.____app____.listen(port=port)
        
        self.____io_loop____.start()
    
    def on_close(self):
        for session in self.world.sessions.values():
            session.connection.close()
        self.____io_loop____.clear_current()
        self.____io_loop____.stop()
        self.____io_loop____ = None


class TornadoServerThread(threading.Thread):
    """_summary_
    
    To avoid the stoppage between pyqt and tornado.
    
    Attributes:
        client: TornadoServiceClient
    """
    def __init__(self, server):
        self.____server____ = server
        
        threading.Thread.__init__(self)

    def run(self):
        self.____server____.on_start()


# if __name__ == "__main__":
#     logging.getLogger().setLevel(logging.DEBUG)
#     test_session = SESession()
#     test_server_app = TornadoServiceServer(test_session)
    
#     try:
#         test_server_app.start()
#     except KeyboardInterrupt:
#         import sys
#         sys.exit()