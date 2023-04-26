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
from core.actor.actor import ActorFactory
from components.teams.team_manager import TeamManager
from components.combats.combat_manager import CombatManager

from utils.helpers.skills_helper import SkillsHelper
from utils.helpers.tasks_helper import TasksHelper
from utils.helpers.npcs_helper import NPCsHelper
from utils.helpers import reload_helper
from utils.singleton_type import SingletonType

from utils.proto.se_world_pb2 import ActorType

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
            if not self.combat_manager.combats:
                break
            
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
    
    def add_a_combat(self, combat_a_id, combat_b_id, npc_combatplan_index=None, running_task=None):
        team_a_id, team_b_id = combat_a_id, combat_b_id
        if "TEAM" not in team_a_id:
            team_a_id = self.team_manager.add_a_team(team_a_id)
        if "TEAM" not in team_b_id:
            if "NPC" in team_b_id:
                npc = ActorFactory.create_actor(ActorType.NPC, self)
                npc.load_proto(self.team_manager.find_a_team(team_a_id).captain, combat_b_id, npc_combatplan_index)
                self.npcs[npc.id] = npc
                team_b_id = npc.id
            team_b_id = self.team_manager.add_a_team(team_b_id)
        
        self.combat_manager.add_a_combat(team_a_id, team_b_id, running_task)


if __name__ == "__main__":
    from tests.attr_test import player_attr
    from actors.player import Player
    from actors.npc import NPC
    
    world = SEWorld(
        skill_file = "F:/CodeProjects/MUD_Game/Server/src/tests/skills.json",
        task_file = "F:/CodeProjects/MUD_Game/Server/src/tests/tasks.json",
        npc_file = "F:/CodeProjects/MUD_Game/Server/src/tests/npcs.json")
    world.players[player_attr.basic_attr.actor_id] = Player(world)
    player = world.players[player_attr.basic_attr.actor_id]
    player.actor_attr = player_attr
    
    # it need to update component attr, pay attention!
    player.id = player_attr.basic_attr.actor_id
    player.skills = player_attr
    player.tasks.tick()
    
    try:
        while True:
            if not world.combat_manager.combats:
                s = input("请输入你的操作：").split(' ')
                if s[0] == "trigger":
                    print(player.tasks.trigger_a_task(s[1], s[2]))
                    print(world.tasks_helper.find_a_task(s[1]).task_process[
                        player.tasks._find_a_running_task(s[1]).curr_index].tp_content)
                elif s[0] == "next":
                    print(player.tasks.task_next_step(s[1], s[2]))
                    try:
                        print(world.tasks_helper.find_a_task(s[1]).task_process[
                            player.tasks._find_a_running_task(s[1]).curr_index].tp_content)
                    except AttributeError:
                        print(player.tasks)
                        print(player.actor_attr)
                elif s[0] == "finish":
                    print(player.tasks.finish_a_task(s[1], s[2]))
                elif s[0] == "show":
                    print(player.tasks)
                elif s[0] == "learn":
                    print(player.skills.learn_skill(s[1]))
                else:
                    print("please check your order!")
                player.tasks.tick()
            else:
                world.tick()
    except KeyboardInterrupt:
        sys.exit()