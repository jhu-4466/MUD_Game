# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: skill tree component
# Author: m14
# Created: 2023.04.17
# Description: a bag component
# History:
#       <autohr>       <version>      <time>        <desc>
#         m14           v0.5        2023/04/18      basic build
# -----------------------------


from core.component.component import Component


class Skill(Component):
    """

    A skill component for the player.

    Args:
        owner (str): The player character who owns this component.
        skill_tree (SkillTreeHelper): A SkillTreeHelper instance to manage the skill tree data.
    """
    component_name: str = "SkillTree"

    def __init__(self, owner):
        super().__init__(owner)
        
        self.current_skills = set()

    def learn_skill(self, target_id: str):
        """

        Learn a new skill.

        Args:
            target_id (str): The ID of the skill to learn.
        Returns:
            bool: True if the skill is learned successfully, False otherwise.
        """
        if target_id in self.current_skills:
            return False
        
        skill_helper = self.owner.world.skill_helper
        target = skill_helper.find_a_skill(target_id)
        if not target:
            return False
        
        # check preconditions
        preconditions = target.preconditions
        if not preconditions:
            self.current_skills.add(target_id)
            return True
        for precondition in preconditions:
            if precondition not in self.current_skills:
                return False
            else:
                continue
        
        self.current_skills.add(target_id)
        return True

    def remove_skill(self, target_id):
        """

        Remove a skill and its child skills from the skill tree.

        Args:
            skill_name (str): The name of the skill to remove.
        Return:
            removes: maybe remove more than one skill due to preconditions.
        """
        removes = set()
        
        skill_helper = self.owner.world.skill_helper
        skills_to_remove = set([target_id])
        while skills_to_remove:
            current_skill_id = skills_to_remove.pop()
            if current_skill_id in self.current_skills:
                removes.add(current_skill_id)
                self.current_skills.remove(current_skill_id)
            
            for learned_id in self.current_skills:
                tmp = skill_helper.find_a_skill(learned_id)
                if current_skill_id in tmp.preconditions:
                    skills_to_remove.add(learned_id)

        return removes