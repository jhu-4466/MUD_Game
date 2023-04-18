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
from utils.helpers import reload_helper
from utils.helpers.skill_helper import SkillHelper


class SEWorld(metaclass=SingletonType):
    """
    
    Holds the world state
    
    Args:
        sessions: tornado connection
    """
    def __init__(self, skill_file):
        self.skill_file = skill_file
        
        self.initialize()
    
    def initialize(self):
        self.sessions = {}
        self.skilltree_helper = None
        
        self.on_initialize()
    
    def on_initialize(self):
        reload_helper.setup()
        
        self.skill_helper = SkillHelper(self.skill_file)
        print(self.skill_helper.standard_skills)
    
    def on_start(self):
        self.tick()
    
    def tick(self):
        """
        
        Cycle through the world state, including db, sessions, and so on
        
        """
        reload_helper.refresh()
    
    def on_close(self):
        self.sessions = {}

    def add_session(self, connection):
        """
        
        Add the session into the game server.

        Args:
            connection: tornado websocket client connection
        """
        new_session = SESession(connection)
        self.sessions[new_session.session_id] = new_session
    
    def remove_session(self, connection):
        """
        
        Remove the session into the game server.
        
        Args:
            connection: tornado websocket client connection
        """
        for id, session in self.sessions.items():
            if session.connection == connection:
                self.sessions.pop(id)
                break
    
    def broadcast(self, message="Hello! My consumer."):
        """
        
        a connect test.
        
        Args:
            message: send message to session.
        """
        for session in self.sessions.values():
            session.connection.write_message(message)