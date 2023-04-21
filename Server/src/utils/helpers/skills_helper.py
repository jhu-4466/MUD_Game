# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: skill tree helper
# Author: m14
# Created: 2023.04.17
# Description: skill tree helper
# History:
#       <autohr>       <version>      <time>        <desc>
#         m14           v0.5        2023/04/18      basic build
#         m14           v0.5        2023/04/19      complete build
# -----------------------------


from utils.proto.se_world_pb2 import SkillAttr

import json
from google.protobuf.json_format import ParseDict


class SkillsHelper:
    """
    
    maintains the standard skills.
    
    Args:
        file_path: skill data file.
        ____standard_skills____: standard all skills.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        
        self.initialize()
    
    def initialize(self):
        self.____standard_skills____ = {}
        
        self.on_initialize()
    
    def on_initialize(self):
        self.load_json()
    
    @property
    def standard_skills(self):
        return self.____standard_skills____
    
    def load_json(self):
        """
        
        load skill data from json.
        
        """
        skills_json = open(self.file_path, 'r', encoding="utf-8")
        skills_data = json.load(skills_json)
        
        for skill_tree in skills_data:
            for skill in skill_tree:
                skill_attr = ParseDict(skill, SkillAttr())
                self.____standard_skills____[skill_attr.skill_id] = skill_attr
        
        skills_json.close()
    
    def find_a_skill(self, skill_id):
        """

        by skill id, finds the skill attr in stanard skill

        Args:
            skill_id (str): the id of a target skill.
        Returns:
            SkillAttr: skill proto message 
        """
        try:
            return self.____standard_skills____[skill_id]
        except:
            return None