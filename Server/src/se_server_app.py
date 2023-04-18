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

import argparse


class SEServerApp:
    """
    
    it controls the tornado server end.
    
    Args:
        world: game world state
        tornado_server: tornado server app
        tornado_server_thread: tornado server thread
    """
    def __init__(self, skill_file):
        self.skill_file = skill_file
        
        self.initialize()
    
    def initialize(self):
        self.world = SEWorld(self.skill_file)
        self.tornado_server = TornadoServiceServer(self.world)
        self.tornado_server_thread = TornadoServerThread(self.tornado_server)
        
    def start(self):
        self.world.on_start()
        
        self.tornado_server_thread.start()
        
        self.tick()
    
    def tick(self):
        """
        
        Cycle through the server state
        
        """
        while True:
            self.world.tick()
        
    def close(self):
        self.tornado_server.on_close()
        self.tornado_server = None
        
        self.world.on_close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-sf", "--skill_file", type=str,
                        required=True, help="standard skill file")
    
    args = parser.parse_args()
    server_app = SEServerApp(args.skill_file)
    try:
        server_app.start()
    except KeyboardInterrupt:
        server_app.close()