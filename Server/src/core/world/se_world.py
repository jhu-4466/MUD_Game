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
# test
import sys
sys.path.append("../../")


from core.session.se_session import SESession

from components.teams.team_manager import TeamManager
from utils.singleton_type import SingletonType
from utils.helpers import reload_helper
from utils.helpers.skills_helper import SkillsHelper

import multiprocessing


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
        # self.process_manager = multiprocessing.Manager()
        # self.players = self.process_manager.dict()
        # self.sessions = self.process_manager.dict()
        self.players = {}
        self.sessions = {}
        
        self.skilltree_helper = None
        self.team_manager = None
        
        self.on_initialize()
    
    def on_initialize(self):
        reload_helper.setup()
        
        self.skill_helper = SkillsHelper(self, self.skill_file)
        
        self.team_manager = TeamManager(self)
        
    def on_start(self):
        self.tick_process = multiprocessing.Process(target=self.tick, daemon=True)
        self.tick_process.start()
    
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
    
    def add_a_combat(self, combat_a_id, combat_b_id):
        team_a_id, team_b_id = combat_a_id, combat_b_id
        if "TEAM" not in team_a_id:
            team_a_id = self.team_manager.add_a_team(team_a_id)
        if "TEAM" not in team_b_id:
            team_b_id = self.team_manager.add_a_team(team_b_id)
        
        return team_a_id, team_b_id


if __name__ == "__main__":
    from tests.attr_test import player_attr, npc_attr
    from actors.player import Player
    
    world = SEWorld("F:/CodeProjects/MUD_Game/Server/src/tests/skills.json")
    world.players[player_attr.basic_attr.actor_id] = Player(world)
    world.players[npc_attr.basic_attr.actor_id] = Player(world)
    player = world.players[player_attr.basic_attr.actor_id]
    npc = world.players[npc_attr.basic_attr.actor_id]
    player.actor_attr = player_attr
    npc.actor_attr = npc_attr
    
    a, b = world.add_a_combat(player.actor_attr.basic_attr.actor_id, npc.actor_attr.basic_attr.actor_id)
    
    world.team_manager.remove_a_team(a)
    world.team_manager.remove_a_team(b)
    
    print(player.actor_attr)
    print(npc.actor_attr)
    