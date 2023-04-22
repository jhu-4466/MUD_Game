# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: team manager component
# Author: m14
# Created: 2023.04.22
# Description: a team manager component that keep track of all team instances.
# History:
#       <autohr>       <version>      <time>        <desc>
#         m14           v0.5        2023/04/      basic build
# -----------------------------


from core.component.component import Component
from components.teams.team import Team

import datetime


class TeamManager(Component):
    """
    
    a team manager component holds on all teams instances in the world.
    
    Args:
        teams: all teams instances in the world.
    """
    component_name: str = "TeamManager"
    
    def __init__(self, owner):
        super().__init__(owner)
        
        self.on_initialize()

    def on_initialize(self):
        self.teams = {}
    
    def add_a_team(self, actor_id):
        """
        
        build a new team

        Args:
            actor_id (str): the captain id
        Returns:
            bool: whether add successfully?
        """
        date_time = datetime.datetime.now()
        team_id = "TEAM" + \
            date_time.strftime("%Y%m%d%H%M%S") + actor_id
        
        self.teams[team_id] = Team(team_id, self.owner.players[actor_id])
        
        return True
    
    def remove_a_team(self, team_id):
        """
        
        remove a team

        Args:
            team_id (str): the team id
        Returns:
            bool: whether add successfully?
        """
        for actor_id in self.teams[team_id].members:
            self.owner.players[actor_id].actor_attr.owned_team_id = ""
        
        self.teams.pop(team_id)
        
        return True