# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: skill tree helper
# Author: m14
# Created: 2023.04.17
# Description: skill tree helper
# History:
#    <autohr>    <version>    <time>        <desc>
#    m14         v0.5         2023/04/    basic build
# -----------------------------

import sys
sys.path.append("../../")

from utils.proto.se_world_pb2 import SkillAttr

from typing import List
import json
from google.protobuf.json_format import ParseDict, MessageToDict


class SkillTreeNode:
    """_summary_
    
    A node in the skill tree.

    Args:
        skill_id (str): The ID of the skill associated with this node.
        children (List[SkillTreeNode]): The child nodes of this node.
    """
    def __init__(self, skill_id: str, skill_attr: SkillAttr):
        self.skill_id = skill_id
        
        self.skill_attr = SkillAttr()
        self.skill_attr.CopyFrom(skill_attr)
        
        self.children = []
    
    def __repr__(self, level=0):
        indent = "\t" * level
        skill_content = MessageToDict(self.skill_attr, preserving_proto_field_name=True)
        output = f"{indent}{skill_content}\n"
        for child in self.children:
            output += child.__repr__(level=level+1)
        return output


class SkillTreeHelper:
    def __init__(self, file_path: str):
        self.standard_skilltree = {}
        
        self.file_path = file_path
        
        self.initialize()
    
    def initialize(self):
        self.on_initialize()
    
    def on_initialize(self):
        self.load_json()
        
    def load_json(self):
        skills_json = open(self.file_path, 'r', encoding="utf-8")
        skills_data = json.load(skills_json)
        
        for skill_tree in skills_data:
            children = skill_tree.pop("children")
            root_attr = ParseDict(skill_tree, SkillAttr())
            root_node = SkillTreeNode(root_attr.skill_id, root_attr)
            self.standard_skilltree[root_attr.skill_id] = root_node
            
            self._add_child_node(root_node, children)

    def _add_child_node(self, parent: SkillTreeNode, children: List[dict]):
        """_summary_
    
        Adds a new skill node to the skill tree.

        Args:
            skill_id (str): The ID of the skill to be added.
            parent_id (str): The ID of the parent skill node. If None, the new node is added as a root node.
        """
        if not children:
            return
        
        for child in children:
            grandchildren = None
            if "children" in child:
                grandchildren = child.pop('children')
            
            child_attr = ParseDict(child, SkillAttr())
            child_node = SkillTreeNode(child_attr.skill_id, child_attr)
            parent.children.append(child_node)
            
            if grandchildren:
                self._add_child_node(child_node, grandchildren)    

if __name__ == "__main__":
    file = "F:/CodeProjects/MUD_Game/Server/src/tests/skills.json"
    
    helper = SkillTreeHelper(file)
    for tree in helper.standard_skilltree.values():
        print(tree)