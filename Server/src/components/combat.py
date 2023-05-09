# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: combat component
# Author: m14
# Created: 2023.04.21
# Description: a combat component
# History:
#       <author>       <version>      <time>        <desc>
#         m14           v0.5        2023/04/24      basic build
#         m14           v0.5        2023/04/25      completed build
# -----------------------------


from core.component.component import Component

from utils.proto.se_world_pb2 import (
    CombatState, NumericAttr, DamageType, CombatInfo, ActorType,
    BuffSituation, BuffType, ChoiceStandard, ChoiceLevel, TaskCombatState)

import time


class Combat(Component):
    """
    
    A component that represents a combat system with similar logic to 阴阳师.
    
    """
    component_name: str = "Combat"

    def __init__(self, owner, combat_id, combat_reward, team_a_id, team_b_id, running_task=None):
        super().__init__(owner)
        
        self.____world____ = self.owner.owner
        
        self.initialize(combat_id, combat_reward, team_a_id, team_b_id, running_task)

    @property
    def world(self):
        return self.____world____

    def initialize(self, combat_id, combat_reward, team_a_id, team_b_id, running_task=None, max_turn_time=30):
        """
        
        Initiates a combat between the specified members.

        Args:
            members (List[Actor]): a list of actor instances participating in the combat.
        """
        self.combat_id = combat_id
        self.combat_state = CombatState.STANDBY
        self.combat_winner = None
        self.combat_reward = combat_reward
        self.combat_task = running_task
        
        self.max_turn_time = max_turn_time
        self.last_buff_time = time.time()
        self.update_buff_flags = False
        
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
        
        team = self.____world____.team_manager.find_a_team(team_id)
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
        if "NPC" in member_id:
            member = self.____world____.npcs[member_id]
        else:
            member = self.____world____.players[member_id]
        # It needs to be loaded with more things, like passive skills influence
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

        curr_time = time.time()
        if curr_time - self.last_buff_time >= 1:
                self.last_buff_time = curr_time
                self.update_buff_flags = True
        for member in self.members.values():
            if self.update_buff_flags:
                self._update_buff_situations(member)
            if self.combat_state == CombatState.RUNNING:
                member.actor_attr.combat_info.turn_time_left -= \
                    delta_time * member.actor_attr.combat_info.combat_numeric.speed
                if member.actor_attr.combat_info.turn_time_left <= 0:
                    self.combat_state = CombatState.STOP
                    self.curr_member_id = member.actor_attr.basic_attr.actor_id
                    self.prompt_member_action(self.curr_member_id)
        self.update_buff_flags = False

    def _update_buff_situations(self, target):
        """
        
        Updates target buffs state.

        Args:
            target (ActorAttr): calculate all buffs in a target.
        """
        for buff in target.actor_attr.combat_info.buff_situations:
            self._calculate_buff_damage(target, buff)
            buff.remain_time -= 1
            if buff.remain_time <= 0:
                target.actor_attr.combat_info.buff_situations.remove(buff)

    def prompt_member_action(self, member_id):
        """
        
        Prompts the specified player to select an action.

        Args:
            member_id (str): the ID of the player being prompted.
        """
        if self.combat_state == CombatState.FINISHED:
            return
        
        if "NPC" in member_id:
            self.apply_npc_action(member_id)
        else:
            # it just is for testing, it need to be changed in the future.
            member_id, target_id, action = input(f"please {member_id} input your action: ").split(' ')
            self.apply_player_action(member_id, target_id, action)

    def apply_npc_action(self, member_id):
        """
        
        Applies the specified action to the specified npcer.

        Args:
            member_id (str): the ID of the member applying the action.
        """
        if member_id != self.curr_member_id:
            return
        
        member = self.members[member_id]
        order = member.actor_attr.combat_orders[member.actor_attr.combat_order_index]
        target = self._judge_npc_target(order)
        
        if not self._apply_action(member, target, order.action_id):
            return
        self._action_finished(member, target)

    def _judge_npc_target(self, order):
        """
        
        judge target for npc

        Args:
            order (NPCCombatOrder): npc combat order
        """
        choice_standard = order.choice_standard
        choice_level = order.choice_standard
        choice_team = order.choice_team
        
        target = None
        for member in self.members.values():
            if member.actor_attr.basic_attr.actor_type != choice_team:
                continue
            if not target:
                target = member
                continue
            
            target = self._judge_npc_target_by_rules(
                target.actor_attr.combat_info.combat_numeric, 
                member.actor_attr.combat_info.combat_numeric, 
                choice_standard, choice_level)

        return target

    def _judge_npc_target_by_rules(self, target, member, standard, level):
        """
        
        judge npc target by order rules

        Args:
            target (CombatNumeric): curr_target combat numeric
            member (CombatNumeric): a new member
            standard (ChoiceStandard): target choice standard
            level (ChoiceLevel): target choice level
        Returns:
            _type_: _description_
        """
        choicestandard_map = {
            ChoiceStandard.SPEED: 'speed',
            ChoiceStandard.PHYSICALDEFENCE: 'physical_defence',
            ChoiceStandard.MAGICALDEFENCE: 'magical_defence',
            ChoiceStandard.HP: 'hp',
            ChoiceStandard.MP: 'mp',
        }
        
        standard_attr = choicestandard_map.get(standard)
        if standard_attr:
            target_value = getattr(target, standard_attr)
            member_value = getattr(member, standard_attr)

            if level == ChoiceLevel.HIGHEST and target_value < member_value:
                return member
            elif level == ChoiceLevel.LOWEST and target_value > member_value:
                return member

    def apply_player_action(self, member_id, target_id, action):
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
            # here return a wrong message
            return
        
        # all actions as skills
        if not self._apply_action(member, target, action):
            return
        self._action_finished(member, target)
    
    def _apply_action(self, member, target, action):
        """
        
        skill action

        Args:
            member (ActorAttr): the attr of the member applying the action.
            target (ActorAttr): the attr of the target.
            action (CombatAction): the action to apply.
        """  
        skill = self.____world____.skills_helper.find_a_skill(action)
        if not self._judge_target_by_skill_rules(member, target, skill):
            return
        skill_level = member.skills.find_a_skill_level(action)
        if not skill_level:
            return
        damage = self.____world____.skills_helper.find_curr_damage(action, skill_level)
        
        # it needs more operations
        if skill.damage_type == DamageType.PHYSICAL:
            self._apply_physical_skill(member, target, damage)
        elif skill.damage_type == DamageType.MAGICAL:
            self._apply_magical_skill(member, target, damage)
        elif skill.damage_type == DamageType.BUFF:
            self._apply_buff_skill(member, target, skill, damage)
        elif skill.damage_type == DamageType.DEBUFF:
            self._apply_buff_skill(member, target, skill, damage)
        
        return True
    
    def _judge_target_by_skill_rules(self, member, choice, skill):
        """
        
        make sure the skill can be effect depends on target team.

        Args:
            member (ActorAttr): member's attr
            choice (ActorAttr): choice's from member attr
            skill (SkillAttr): skill attr
        Returns:
            bool: if skill can not influent target team returns False, otherwise returns True
        """
        if not skill:
            return False
        
        member_type = member.actor_attr.basic_attr.actor_type
        choice_type = choice.actor_attr.basic_attr.actor_type
        targetteam_map = {
            DamageType.PHYSICAL: ActorType.NPC if member_type == ActorType.PLAYER else ActorType.PLAYER,
            DamageType.MAGICAL: ActorType.NPC if member_type == ActorType.PLAYER else ActorType.PLAYER,
            DamageType.BUFF: ActorType.PLAYER if member_type == ActorType.PLAYER else ActorType.NPC,
            DamageType.DEBUFF: ActorType.NPC if member_type == ActorType.PLAYER else ActorType.PLAYER,
        }
        
        target_team = targetteam_map.get(skill.damage_type)
        if choice_type != target_team:
            return False
        
        return True
    
    def _apply_physical_skill(self, member, target, damage):
        """
        
        apply a physical skill, including normal attack

        Args:
            member (ActorAttr): the attr of the member applying the action.
            target (ActorAttr): the attr of the target.
            damage (CombatAction): skill damage in one level, but not player.
        """
        target.actor_attr.combat_info.combat_numeric.hp -= \
            int(damage * member.actor_attr.combat_info.combat_numeric.physical_damage)
    
    def _apply_magical_skill(self, member, target, damage):
        """
        
        apply a magical skill

        Args:
            member (ActorAttr): the attr of the member applying the action.
            target (ActorAttr): the attr of the target.
            damage (CombatAction): skill damage in one level, but not player.
        """     
        target.actor_attr.combat_info.combat_numeric.hp -= \
            int(damage * member.actor_attr.combat_info.combat_numeric.magical_damage)
    
    def _apply_buff_skill(self, member, target, buff, damage):
        """
        
        apply a buff skill, including normal attack
        the same buff skill can not add again

        Args:
            member (ActorAttr): the attr of the member applying the action.
            target (ActorAttr): the attr of the target.
            buff (SkillAttr): a buff skill
            damage (CombatAction): skill damage in one level, but not player.
        """
        for _ in target.actor_attr.combat_info.buff_situations:
            if _.skill_id == buff.skill_id:
                return
        
        buff_situation = BuffSituation()
        buff_situation.skill_id = buff.skill_id
        buff_situation.buff_type = buff.buff_type
        buff_situation.remain_time = buff.duration
        buff_situation.damage = int(
            damage * member.actor_attr.combat_info.combat_numeric.magical_damage)

        target.actor_attr.combat_info.buff_situations.append(buff_situation)
        self._calculate_buff_damage(target, buff_situation)
    
    def _calculate_buff_damage(self, target, buff):
        """
        
        calculate buff damage

        Args:
            target (ActorAttr): the attr of the target.
            buff (BuffSituation): a buff on target
        """ 
        if buff.buff_type == BuffType.TREATMENT:
            target.actor_attr.combat_info.combat_numeric.hp += buff.damage
        elif buff.buff_type == BuffType.HAEMORRHAGE:
            target.actor_attr.combat_info.combat_numeric.hp -= buff.damage
        else:
            pass
        
        if target.actor_attr.combat_info.combat_numeric.hp <= 0:
            self.members_state[target.actor_attr.owned_team_id] -= 1
        self._check_combat_state()
    
    def _action_finished(self, member, target):
        if target.actor_attr.combat_info.combat_numeric.hp <= 0:
            self.members_state[target.actor_attr.owned_team_id] -= 1
        self.curr_member_id = None
        member.actor_attr.combat_info.turn_time_left = self.max_turn_time
        self._check_combat_state()
    
    def _check_combat_state(self):
        """
        
        checks combat state during every action.
        
        """        
        for team_id, alive_amount in self.members_state.items():
            if alive_amount == 0:
                self.combat_winner = [team for team in self.members_state.keys() if team != team_id][0]
                self.combat_state = CombatState.FINISHED
                self._distribute_reward()
                self._destroy_instance()
                return

        self.combat_state = CombatState.RUNNING
    
    def _destroy_instance(self):
        """
        
        after combat, destory the combat instance autoly.
        
        """
        self._destroy_npcs()
        self.owner.remove_a_combat(self)
            
    def _destroy_npcs(self):
        """
        
        after combat, destory npcs in the combat.
        
        """
        if self.combat_state != CombatState.FINISHED:
            return
        
        for member_id, member in self.members.items():
            if member.actor_attr.basic_attr.actor_type == ActorType.NPC:
                npc = self.world.npcs.pop(member_id)
                del npc
    
    def _distribute_reward(self):
        """
        
        after combat, distribute reward.
        save reward in the server directly, just add a other_info attr to client.
        
        """
        if 'NPC' in self.combat_winner:
            return
        
        print(self.combat_winner)
        self.combat_task.combat_state = TaskCombatState.WIN
        
        team = self.____world____.team_manager.find_a_team(self.combat_winner)
        for member_id in team.members:
            pass