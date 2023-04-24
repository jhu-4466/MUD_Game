# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: combat component
# Author: m14
# Created: 2023.04.21
# Description: a combat component
# History:
#       <autohr>       <version>      <time>        <desc>
#         m14           v0.5        2023/04/24      basic build
# -----------------------------


from core.component.component import Component

from utils.proto.se_world_pb2 import CombatState, NumericAttr, CombatActionType, DamageType, CombatAction, CombatInfo
from google.protobuf.json_format import ParseDict
import json


class Combat(Component):
    """
    
    A component that represents a combat system with similar logic to 阴阳师.
    
    """
    component_name: str = "Combat"

    def __init__(self, owner, combat_id, combat_reward, team_a_id, team_b_id):
        super().__init__(owner)
        
        self.initialize(combat_id, combat_reward, team_a_id, team_b_id)

    def initialize(self, combat_id, combat_reward, team_a_id, team_b_id, max_turn_time=100):
        """
        
        Initiates a combat between the specified members.

        Args:
            members (List[Actor]): a list of actor instances participating in the combat.
        """
        self.combat_id = combat_id
        self.combat_state = CombatState.STANDBY
        self.combat_winner = None
        self.combat_reward = combat_reward
        
        self.max_turn_time = max_turn_time
        
        self.actions = []
        self.members = {}
        self.members_state = {}
        self.curr_member_id = None
        
        self.on_initialize(team_a_id, team_b_id)

    def on_initialize(self, team_a_id, team_b_id):
        """
        
        Event triggered when a combat starts.
        
        """
        self.members.update(self._get_all_members(team_a_id))
        self.members.update(self._get_all_members(team_b_id))
        
        self.combat_state = CombatState.RUNNING

    def _get_all_members(self, team_id):
        """_summary_

        Args:
            team_id (str): the id of a team.
        Returns:
            members: members in the team.
        """
        members = {}
        
        team = self.owner.owner.team_manager.find_a_team(team_id)
        for member_id in team.members:
            member = self._get_player_state(member_id)
            members[member_id] = member
            if team_id not in self.members_state:
                self.members_state[team_id] = 0
            self.members_state[team_id] += 1

        return members

    def _get_player_state(self, member_id):
        """
        
        Returns the state of the specified player.

        Args:
            member_id (str): the ID of the player to get the state for.
        Returns:
            member_attr: a ActorAttr message.
        """
        # It needs to be loaded with more things, like passive skills influence
        member = self.owner.owner.players[member_id]
        combat_numeric = NumericAttr()
        combat_numeric.CopyFrom(member.actor_attr.numeric_attr)
        combat_info = CombatInfo()
        combat_info.combat_numeric.CopyFrom(combat_numeric)
        member.actor_attr.combat_info.CopyFrom(combat_info)
        member.actor_attr.combat_info.turn_time_left = self.max_turn_time
        
        return member

    def is_finished(self):
        return self.combat_state

    def tick(self, delta_time: int):
        """
        Updates the combat state.

        Args:
            delta_time (int): the time since the last update.
        """
        if self.combat_state != CombatState.RUNNING:
            if self.combat_state == CombatState.STOP:
                self.prompt_member_action(self.curr_member_id)
            return

        for member in self.members.values():
            if self.combat_state == CombatState.RUNNING:
                member.actor_attr.combat_info.turn_time_left -= \
                    int(delta_time * member.actor_attr.combat_info.combat_numeric.speed)
                if member.actor_attr.combat_info.turn_time_left <= 0:
                    self.combat_state = CombatState.STOP
                    self.curr_member_id = member.actor_attr.basic_attr.actor_id
                    self.prompt_member_action(self.curr_member_id)

    def prompt_member_action(self, member_id):
        """
        Prompts the specified player to select an action.

        Args:
            member_id (str): the ID of the player being prompted.
        """
        if self.combat_state == CombatState.FINISHED:
            return
        
        member_id, target_id, action = input(f"please {member_id} input your action: ").split(' ')
        action = ParseDict(json.loads(action), CombatAction())
        
        self.apply_action(member_id, target_id, action)

    def apply_action(self, member_id, target_id, action):
        """
        Applies the specified action to the specified player.

        Args:
            member_id (str): the ID of the member applying the action.
            target_id (str): the id of the target.
            action (CombatAction): the action to apply.
        """
        if member_id != self.curr_member_id:
            return
        member = self.members[member_id]
        target = self.members[target_id]
        if member.actor_attr.combat_info.turn_time_left > 0:
            return
        
        if action.action_type == CombatActionType.NORMAL:
            self._apply_normal_action(member, target)
        elif action.action_type == CombatActionType.SKILL:
            self._apply_skill_action(member, target, action)
        self.curr_member_id = None
        member.actor_attr.combat_info.turn_time_left = self.max_turn_time
        
        if target.actor_attr.combat_info.combat_numeric.hp <= 0:
            self.members_state[target.actor_attr.owned_team_id] -= 1

        self.check_combat_state()
    
    def _apply_normal_action(self, member, target):
        """
        
        normal action

        Args:
            member (ActorAttr): the attr of the member applying the action.
            target (ActorAttr): the attr of the target.
        """        
        target.actor_attr.combat_info.combat_numeric.hp -= \
            member.actor_attr.combat_info.combat_numeric.physical_damage
    
    def _apply_skill_action(self, member, target, action):
        """
        
        normal action

        Args:
            member (ActorAttr): the attr of the member applying the action.
            target (ActorAttr): the attr of the target.
        """      
        skill = self.owner.owner.skills_helper.find_a_skill(action.skill_id)
        skill_level = member.skills.find_a_skill(action.skill_id)
        print(member.actor_attr)
        print(member.skills)
        if not skill_level:
            return
        
        # it needs more operations
        if skill.damage_type == DamageType.PHYSICAL:
            target.actor_attr.combat_info.combat_numeric.hp -= \
                skill.damage[skill_level - 1] * member.actor_attr.combat_info.combat_numeric.physical_damage
        elif skill.damage_type == DamageType.MAGICAL:
            target.actor_attr.combat_info.combat_numeric.hp -= \
                skill.damage[skill_level - 1] * member.actor_attr.combat_info.combat_numeric.magical_damage
        elif skill.damage_type == DamageType.BUFF:
            pass
        elif skill.damage_type == DamageType.DEBUFF:
            pass
            
        print(target.actor_attr.combat_info.combat_numeric.hp)
    
    def check_combat_state(self):
        """
        
        checks combat state during every action.
        
        """        
        for team_id, alive_amount in self.members_state.items():
            if alive_amount == 0:
                self.combat_winner = [team for team in self.members_state.keys() if team != team_id][0]
                self.combat_state = CombatState.FINISHED
                return

        self.combat_state = CombatState.RUNNING
    
    def distribute_reward(self):
        """
        
        after combat, distribute reward.
        save reward in the server directly, just add a other_info attr to client.
        
        """
        team = self.owner.owner.team_manager.find_a_team(self.combat_winner)
        
        for member_id in team.members:
            pass