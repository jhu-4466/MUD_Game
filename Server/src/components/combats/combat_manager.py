# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: combat manager component
# Author: m14
# Created: 2023.04.22
# Description: a combat manager component that keep track of all combat instances.
# History:
#       <author>       <version>      <time>        <desc>
#         m14           v0.5        2023/04/24      basic build
# -----------------------------


from core.component.component import Component
from components.combats.combat import Combat

from utils.proto.se_world_pb2 import CombatState

import datetime


class CombatManager(Component):
    """

    A component that manages all combat instances happening in the world.
    
    Args:
        owner(str): belongs to one world.
    """
    component_name: str = "CombatManager"
    activate_flag: bool = False

    def __init__(self, owner):
        super().__init__(owner)
        
        self.combats = []  # A dictionary to store all combat instances

    def add_a_combat(self, team_a_id, team_b_id, running_task):
        """
        Add a new combat instance to the scene.

        Args:
            team_a_id (Player): must player team.
            team_b_id (NPC / Player): must npc team or other player team.
        """
        combat_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + \
            f"{team_a_id}_{team_b_id}"
        combat_instance = Combat(self, combat_id, None, team_a_id, team_b_id, running_task)
        self.combats.append(combat_instance)

    def remove_a_combat(self, combat):
        """
        Remove a combat instance from the scene.

        Args:
            combat: a combat instance
        """
        print('????')
        self.combats.remove(combat)
        del combat

    def tick(self, delta_time):
        """
        Update all combat instances in the scene.

        Args:
            delta_time (int): The time elapsed since the last update.
        """
        for combat in self.combats:
            if combat.is_finished() == CombatState.FINISHED:
                combat.distribute_reward()
                self.remove_a_combat(combat)
                continue
            combat.tick(delta_time)