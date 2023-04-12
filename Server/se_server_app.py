# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: game server controlling all.
# Author: m14
# Created: 2023.04.11
# Description: maintains game server and tornado server.
# History:
#    <autohr>    <version>    <time>        <desc>
#    m14         v0.1         2023/04/12    basic build
# -----------------------------


from core.world.se_world import SEWorld
from services.tornado_service_server import TornadoServiceServer, TornadoServerThread

import threading

import sys
import logging


class SEServerApp:
    def __init__(self):
        self.initialize()
    
    def initialize(self):
        logging.basicConfig(level=logging.DEBUG, 
            format="[%(asctime)s] - [%(levelname)s] - %(message)s")
        self.tornado_logger = logging.getLogger('tornado')
        
        self.world = SEWorld()
        self.tornado_server = TornadoServiceServer(self.world, self.tornado_logger)
        self.tornado_server_thread = TornadoServerThread(self.tornado_server)
        
    def start(self):
        self.world.on_start()
        
        self.tornado_server_thread.start()
        
        self.tick()
    
    def tick(self):
        while True:
            self.world.tick()

    def close(self):
        self.tornado_server.on_close()
        self.tornado_server = None
        
        self.world.on_close()

if __name__ == '__main__':
    server_app = SEServerApp()
    try:
        server_app.start()
    except KeyboardInterrupt:
        server_app.close()
        sys.exit()