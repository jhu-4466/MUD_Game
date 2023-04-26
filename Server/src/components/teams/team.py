# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: team component
# Author: m14
# Created: 2023.04.21
# Description: a team component
# History:
#       <autohr>       <version>      <time>        <desc>
#         m14           v0.5        2023/04/      basic build
# -----------------------------


from core.component.component import Component


class Team(Component):
    """
    
    a team component holds on all players or npcs in one team
    
    Args:
        team_id: a guid in the world based on datetime and captain id.
        captain: holds the captain id.
        members: holds all members id.
    """
    component_name: str = "Team"
    
    def __init__(self, team_id, player):
        self.____team_id____ = team_id
        
        self.captain = None
        self.members = set()
        
        self.on_initialize(player)

    def on_initialize(self, player):
        actor_id = player.id
        
        self.captain = actor_id
        self.members.add(actor_id)
        player.actor_attr.owned_team_id = self.____team_id____
    
    @property
    def team_id(self):
        return self.____team_id____