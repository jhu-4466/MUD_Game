# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: skill tree component
# Author: m14
# Created: 2023.04.17
# Description: a bag component
# History:
#       <autohr>       <version>      <time>        <desc>
#         m14           v0.5        2023/04/17      basic build
# -----------------------------


from core.component.component import Component

from utils.helpers.skilltree_helper import SkillTreeHelper, SkillTreeNode
from utils.proto.se_world_pb2 import SkillAttr


class SkillTree(Component):
    """_summary_
    
    The SkillTree component class.

    Args:
        component_name (str): The name of the component.
        skill_tree (dict): A dictionary representing the skill tree, with skill IDs as keys and SkillTreeNode objects
            as values.
    """

    component_name = "SkillTree"

    def __init__(self, owner):
        """_summary_
    
        Initializes a new instance of the SkillTree class.

        Args:
            owner: The owner of the component.
        """
        super().__init__(owner)
        self.skill_tree = {}

    def _find_node_by_skill(self, node: SkillTreeNode, skill_id: str):
        """Recursively searches for a node.

        Args:
            node (SkillNode): The current node being searched.
            skill_id (str): The ID of the skill to find.
        Returns:
            The node with the specified skill ID, or None if it is not found.
        """
        if node.skill_id == skill_id:
            return node

        for child in node.children:
            result = self._find_node_by_skill(child, skill_id)
            if result is not None:
                return result

        return None

    def add_skill(self, skill_id: str, parent_id: str = None):
        """_summary_
    
        Adds a new skill node to the skill tree.

        Args:
            skill_id (str): The ID of the skill to be added.
            parent_id (str): The ID of the parent skill node. If None, the new node is added as a root node.
        """
        node = SkillTreeNode(skill_id)
        if parent_id:
            parent_node = self._find_node_by_skill(parent_id)
            if parent_node:
                parent_node.children.append(node)
        else:
            if skill_id in self.skill_tree:
                return
            self.skill_tree[skill_id] = node

    def remove_skill(self, skill_id: str):
        """_summary_
    
        Removes a skill node from the skill tree.

        Args:
            skill_id (str): The ID of the skill node to be removed.
        """
        node = self.skill_tree.pop(skill_id, None)
        if node:
            for parent_node in self.skill_tree.values():
                for child_node in parent_node.children:
                    if child_node.skill_id == skill_id:
                        parent_node.children.remove(child_node)
                        parent_node.children.extend(child_node.children)

    def get_skill_parents(self, skill_id: str):
        """_summary_
    
        Returns a list of the IDs of all parent nodes for the specified skill.

        Args:
            skill_id (str): The ID of the skill node.
        Returns:
            A list of the IDs of all parent nodes for the specified skill.
        """
        parents = []
        for node_id, node in self.skill_tree.items():
            for child_node in node.children:
                if child_node.skill_id == skill_id:
                    parents.append(node_id)
        return parents

    def get_skill_children(self, skill_id: str):
        """_summary_
    
        Returns a list of the IDs of all child nodes for the specified skill.

        Args:
            skill_id (str): The ID of the skill node.
        Returns:
            A list of the IDs of all child nodes for the specified skill.
        """
        node = self.skill_tree.get(skill_id)
        if node:
            return [child_node.skill_id for child_node in node.children]
        return []

    def tick(self, delta_time):
        """_summary_
    
        Updates the skill state, if someone has duration or cooldown.

        Args:
            delta_time: The time elapsed since the last update.
        """
        pass

    def load_proto(self, value):
        """_summary_
    
        Loads the skill tree information from a protobuf object.

        Args:
            value: The protobuf object containing the skill tree information.
        """
        pass