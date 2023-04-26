# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: skill tree component
# Author: m14
# Created: 2023.04.17
# Description: a bag component
# History:
#       <autohr>       <version>      <time>        <desc>
#         m14           v0.5        2023/04/18      basic build
#         m14           v0.5        2023/04/19      complete build
# -----------------------------


from core.component.component import Component
from utils.proto.se_world_pb2 import SkillAttr, LearnedSkill


class Skills(Component):
    """

    A skill component for the player.

    Args:
        owner (str): The player character who owns this component.
        learned_skills (LearnedSkill): skill have been learned.
    """
    component_name: str = "Skills"

    def __init__(self, owner):
        super().__init__(owner)
        
        self.learned_skills = self.owner.actor_attr.learned_skills
        self.skills_helper = self.owner.world.skills_helper
    
    def load_proto(self, value):
        """
        
        update attr from proto data.

        Args:
            value (ActorAttr): actor attr.
        """        
        self.learned_skills = value.learned_skills
    
    def learn_skill(self, target_id: str):
        """

        Learn a new skill.

        Args:
            target_id (str): The ID of the skill to learn.
        Returns:
            bool: True if the skill is learned successfully, False otherwise.
        """
        if target_id in self.learned_skills or self.owner.actor_attr.skill_points < 1:
            return False
        
        target_skill = SkillAttr()
        find_result = self.skills_helper.find_a_skill(target_id)
        if not find_result:
            return False
        target_skill.CopyFrom(find_result)
        
        # check preconditions
        preconditions = target_skill.preconditions
        if not preconditions:
            target = LearnedSkill(skill_id=target_id, curr_skill_level=1)
            self.owner.actor_attr.skill_points -= 1
            self.learned_skills.append(target)
            return True
        for precondition in preconditions:
            learned_skills_ids = self._find_learned_skills_ids()
            if precondition not in learned_skills_ids:
                return False
            else:
                continue
            
        target = LearnedSkill(skill_id=target_id, curr_skill_level=1)
        self.owner.actor_attr.skill_points -= 1
        self.learned_skills.append(target)
        return True

    def remove_skill(self, target_id):
        """

        Remove a skill and its child skills from the skill tree.

        Args:
            target_id (str): The ID of the skill to remove.
        Returns:
            bool: True if the skill is removed successfully, False otherwise.
        """
        to_remove_ids = set([target_id])
        while to_remove_ids:
            curr_remove_id = to_remove_ids.pop()

            after_remove_skills = []
            for learned_skill in self.learned_skills:
                if learned_skill.skill_id != curr_remove_id:
                    after_remove_skills.append(learned_skill)
                else:
                    self.owner.actor_attr.skill_points += learned_skill.curr_skill_level
            self.learned_skills = after_remove_skills
            
            for learned_skill in self.learned_skills:
                tmp = self.skills_helper.find_a_skill(learned_skill.skill_id)
                if curr_remove_id in tmp.preconditions:
                    to_remove_ids.add(learned_skill.skill_id)
        
        return True

    def upgrade_skill_levels(self, target_id, upgrade_count):
        """
        
        upgrade skill levels.

        Args:
            target_id (str): upgrade target skill level
            upgrade_count (int): upgrade counts.
        Returns:
            a bool means whether upgrade successfully.
        """
        if self.owner.actor_attr.skill_points < upgrade_count:
            return False
        
        target_skill = self.skills_helper.find_a_skill(target_id)
        for learned_skill in self.learned_skills:
            if learned_skill.skill_id != target_skill.skill_id:
                continue
            
            if learned_skill.curr_skill_level + upgrade_count < target_skill.max_skill_level:
                learned_skill.curr_skill_level += upgrade_count
                self.owner.actor_attr.skill_points -= upgrade_count
                return True
            else:
                self.owner.actor_attr.skill_points -= target_skill.max_skill_level - learned_skill.curr_skill_level
                learned_skill.curr_skill_level = target_skill.max_skill_level
                return True
            
        return False
    
    def demote_skill_levels(self, target_id, demote_count):
        """
        
        demote skill levels.

        Args:
            target_id (str): demote target skill level
            demote_count (int): demote counts.
        Returns:
            a bool means whether demote successfully.
        """
        target_skill = self.skills_helper.find_a_skill(target_id)
        for learned_skill in self.learned_skills:
            if learned_skill.skill_id != target_skill.skill_id:
                continue
            
            if learned_skill.curr_skill_level >= demote_count:
                learned_skill.curr_skill_level -= demote_count
                self.owner.actor_attr.skill_points += demote_count
                if learned_skill.curr_skill_level == 0:
                    self.remove_skill(target_id)
                return True
            
        return False

    def reset_skills(self):
        """
        
        reset actor skill.
        
        """
        while self.learned_skills:
            curr_remove_skill = self.learned_skills.pop()
            self.owner.actor_attr.skill_points += curr_remove_skill.curr_skill_level
            self.remove_skill(curr_remove_skill.skill_id)
        
        return True
    
    def find_a_skill_level(self, target_id):
        """
        
        find the curr level of the skill
        
        Args:
            target_id: target skill id.
        """
        for skill in self.learned_skills:
            if skill.skill_id == target_id:
                return skill.curr_skill_level
        
        return None
    
    def find_highest_skill_level(self):
        """
        
        find the highest skill level

        """
        highest_level = 0
        
        for skill in self.learned_skills:
            highest_level = \
                skill.curr_skill_level if highest_level <= skill.curr_skill_level else highest_level
        
        return highest_level
    
    def _find_learned_skills_ids(self):
        """
        
        find actor's learned skills ids.
        
        Returns:
            ids: actor's learned skills ids.
        """
        ids = set()
        
        for skill in self.learned_skills:
            ids.add(skill.skill_id)
        
        return ids
    
    def __repr__(self):
        output = "已学技能：\n"
        
        for learned_skill in self.learned_skills:
            skill_attr = self.skills_helper.find_a_skill(learned_skill.skill_id)
            output += f"{skill_attr.skill_name}({learned_skill.skill_id}): {skill_attr.skill_desc}\n"
            output += f"\t当前等级: {learned_skill.curr_skill_level}\n"
        
        return output