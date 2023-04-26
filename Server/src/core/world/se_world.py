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
from components.combats.combat_manager import CombatManager
from utils.helpers.skills_helper import SkillsHelper
from utils.helpers.tasks_helper import TasksHelper
from utils.helpers.npcs_helper import NPCsHelper

from utils.singleton_type import SingletonType
from utils.helpers import reload_helper

import multiprocessing


class SEWorld(metaclass=SingletonType):
    """
    
    Holds the world state
    
    Args:
        sessions: tornado connection
    """
    def __init__(self, npc_file, skill_file, task_file):
        self.npc_file = npc_file
        self.skill_file = skill_file
        self.task_file = task_file
        
        self.initialize()
    
    def initialize(self):
        # self.process_manager = multiprocessing.Manager()
        # self.players = self.process_manager.dict()
        # self.sessions = self.process_manager.dict()
        self.players = {}
        self.npcs = {}
        self.sessions = {}
        
        self.skilltree_helper = None
        self.tasks_helper = None
        self.npcs_helper = None
        
        self.team_manager = None
        self.combat_manager = None
        
        self.on_initialize()
    
    def on_initialize(self):
        reload_helper.setup()
        
        self.npcs_helper = NPCsHelper(self, self.npc_file)
        self.tasks_helper = TasksHelper(self, self.task_file)
        self.skills_helper = SkillsHelper(self, self.skill_file)
        
        self.team_manager = TeamManager(self)
        self.combat_manager = CombatManager(self)
        
    def on_start(self):
        self.tick_process = multiprocessing.Process(target=self.tick, daemon=True)
        self.tick_process.start()
    
    def tick(self):
        """
        
        Cycle through the world state, including db, sessions, and so on
        
        """
        while True:
            # reload_helper.refresh()
            
            self.combat_manager.tick(1 / 30)
    
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
        
        self.combat_manager.add_a_combat(team_a_id, team_b_id)


if __name__ == "__main__":
    from tests.attr_test import player_attr, npc_attr
    from actors.player import Player
    from actors.npc import NPC
    
    world = SEWorld(
        skill_file="F:/CodeProjects/MUD_Game/Server/src/tests/skills.json",
        task_file="F:/CodeProjects/MUD_Game/Server/src/tests/tasks.json")
    world.players[player_attr.basic_attr.actor_id] = Player(world)
    world.npcs[npc_attr.basic_attr.actor_id] = NPC(world)
    player = world.players[player_attr.basic_attr.actor_id]
    npc = world.npcs[npc_attr.basic_attr.actor_id]
    player.actor_attr = player_attr
    npc.actor_attr = npc_attr
    
    # it need to update component attr, pay attention!
    player.skills = player_attr
    npc.skills = npc_attr

    world.add_a_combat(player.actor_attr.basic_attr.actor_id, npc.actor_attr.basic_attr.actor_id)

    try:   
        world.tick()
    except KeyboardInterrupt:
        sys.exit()
    