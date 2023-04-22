# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: combat manager component
# Author: m14
# Created: 2023.04.22
# Description: a combat manager component that keep track of all combat instances.
# History:
#       <autohr>       <version>      <time>        <desc>
#         m14           v0.5        2023/04/      basic build
# -----------------------------


from core.component.component import Component
from components.combats.combat import Combat


class CombatScene(Component):
    """

    A component that manages all combat instances happening in a scene.
    
    Args:
        owner(str): belongs to one scene.
    """
    component_name: str = "CombatScene"
    activate_flag: bool = False

    def __init__(self, owner):
        super().__init__(owner)
        
        self.combats = {}  # A dictionary to store all combat instances

    def add_a_combat(self, team_a, team_b):
        """
        Add a new combat instance to the scene.

        Args:
            player (Player): The player object participating in the combat.
            npc (NPC): The NPC object participating in the combat.
        """
        combat_id = f"{team_a.team_id}_{team_b.team_id}"
        new_combat_instance = Combat(players)
        self.combats[combat_id] = new_combat_instance

    def remove_a_combat(self, player, npc):
        """
        Remove a combat instance from the scene.

        Args:
            player (Player): The player object participating in the combat.
            npc (NPC): The NPC object participating in the combat.
        """
        combat_id = f"{player.actor_id}_{npc.actor_id}"
        del self.combats[combat_id]

    def get_combat_instance(self, player, npc):
        """
        Retrieve a combat instance from the scene.

        Args:
            player (Player): The player object participating in the combat.
            npc (NPC): The NPC object participating in the combat.

        Returns:
            The CombatInstance object corresponding to the input player and NPC.
        """
        combat_id = f"{player.actor_id}_{npc.actor_id}"
        return self.combats.get(combat_id)

    def tick(self, delta_time):
        """
        Update all combat instances in the scene.

        Args:
            delta_time (int): The time elapsed since the last update.
        """
        for combat in self.combats.values():
            finish_sign = combat.tick(delta_time)
            if finish_sign:
                self.remove_a_combat(combat)