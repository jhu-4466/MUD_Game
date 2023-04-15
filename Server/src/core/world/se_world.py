# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: sky eye world state
# Author: m14
# Created: 2023.04.11
# Description: maintains sky eye world state
# History:
#    <autohr>    <version>    <time>        <desc>
#    m14         v0.1         2023/04/11    basic build
# -----------------------------


from core.session.se_session import SESession

from utils.singleton_type import SingletonType
from utils import reload_helper


class SEWorld(metaclass=SingletonType):
    """_summary_
    
    Holds the world state
    
    Attributes:
        sessions: tornado connection
    """
    def __init__(self):
        self.initialize()
    
    def initialize(self):
        self.sessions = {}
        
        reload_helper.setup()
    
    def on_start(self):
        self.tick()
    
    def tick(self):
        """_summary_
        
        Cycle through the world state, including db, sessions, and so on
        
        """
        reload_helper.refresh()
    
    def on_close(self):
        self.sessions = {}

    def add_session(self, connection):
        """_summary_
        
        Add the session into the game server.

        Attributes:
            connection: tornado websocket client connection
        """
        new_session = SESession(connection)
        self.sessions[new_session.session_id] = new_session
    
    def remove_session(self, connection):
        """_summary_
        
        Remove the session into the game server.
        
        Attributes:
            connection: tornado websocket client connection
        """
        for id, session in self.sessions.items():
            if session.connection == connection:
                self.sessions.pop(id)
                break
    
    def broadcast(self, message="Hello! My consumer."):
        """_summary_
        
        a connect test.
        
        Attributes:
            message: send message to session.
        """
        for session in self.sessions.values():
            session.connection.write_message(message)