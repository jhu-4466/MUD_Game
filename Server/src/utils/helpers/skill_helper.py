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
import sys, os

from utils.singleton_type import SingletonType
from utils.proto.se_world_pb2 import SkillAttr

import json
from google.protobuf.json_format import ParseDict


class SkillHelper(metaclass=SingletonType):
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
        skills_json = open(self.file_path, 'r', encoding="utf-8")
        skills_data = json.load(skills_json)
        
        for skill_tree in skills_data:
            for skill in skill_tree:
                skill_attr = ParseDict(skill, SkillAttr())
                self.____standard_skills____[skill_attr.skill_id] = skill_attr
    
    def find_a_skill(self, skill_id):
        return self.____standard_skills____[skill_id]


if __name__ == "__main__":
    s = SkillHelper("F:/CodeProjects/MUD_Game/Server/src/tests/skills.json")