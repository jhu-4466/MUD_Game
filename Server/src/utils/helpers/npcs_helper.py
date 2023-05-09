# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: NPCs helper
# Author: m14
# Created: 2023.04.26
# Description: NPCs helper
# History:
#       <author>       <version>      <time>        <desc>
#         m14           v0.5        2023/04/26      basic build
# -----------------------------


from utils.proto.se_world_pb2 import NPCAttr

from google.protobuf.json_format import ParseDict
import json


class NPCsHelper:
    """
    
    maintains the standard tasks.
    
    Args:
        owner: the game world
        file_path: tasks data file.
        ____standard_npcs____: standard all tasks.
    """
    def __init__(self, owner, file_path):
        self.owner = owner
        self.file_path = file_path
        
        self.initialize()
    
    def initialize(self):
        self.____standard_npcs____ = {}
        
        self.on_initialize()

    def on_initialize(self):
        self.load_json()

    @property
    def standard_npcs(self):
        return self.____standard_npcs____

    def load_json(self):
        """
        
        load npcs data from json.
        
        """
        npcs_json = open(self.file_path, 'r', encoding="utf-8")
        npcs_data = json.load(npcs_json)

        for npc in npcs_data:
            npc_attr = ParseDict(npc, NPCAttr())
            self.____standard_npcs____[npc_attr.basic_attr.actor_id] = npc_attr
        
        npcs_json.close()
    
    def find_a_npc(self, npc_id):
        """

        by npc id, finds the npc attr in stanard npc

        Args:
            npc_id (str): the id of a target npc.
        Returns:
            TaskAttr: npc proto message 
        """
        try:
            return self.____standard_npcs____[npc_id]
        except:
            return None


if __name__ == "__main__":
    a = NPCsHelper(None, "D:/liuyuqi/SkyEye/MUD_Game/Server/src/tests/npcs.json")
    
    print(a.standard_npcs)