# -*- coding: utf-8 -*-
 
# -----------------------------
# Topic: items_helper.py
# Author: 
# Created: 2023/05/06
# Description: 
# History:
#    <autohr>    <version>    <time>        <desc>
#    liuyuqi      v0.5.0      2023/05/06   basic build
# -----------------------------


from utils.proto.se_world_pb2 import ItemAttr

from google.protobuf.json_format import ParseDict
import json


class ItemsHelper:
    """
    
    maintains the item information.
    self.____standard_items____ = { item_id: item_attr,...}
    
    Args:
        owner: the game world
        file_path: items data file.
        ____standard_items____: standard all items.
    """
    def __init__(self, owner, file_path: str):
        self.owner = owner
        self.file_path = file_path
        
        self.initialize()
    
    def initialize(self):
        self.____standard_items____ = {}
        
        self.on_initialize()
    
    def on_initialize(self):
        self.load_json()
    
    @property
    def standard_items(self):
        return self.____standard_items____
    
    def load_json(self):
        """
        
        load items data from json.
        
        """
        items_json = open(self.file_path, 'r', encoding="utf-8")
        items_data = json.load(items_json)
        
        for item in items_data:
            item_attr = ParseDict(item, ItemAttr())
            self.standard_items[item_attr.item_id] = item_attr
        items_json.close()
    
    def find_a_price(self, item_id):
        try:
            return self.____standard_items____[item_id].price
        except:
            return None
        
    
    
    def find_a_item_attr(self, item_id):
        """

        by item_id, finds the item attr in stanard item

        Args:
            item_id (str): the id of a target item.
        Returns:
            ItemAttr: item proto message 
        """
        try:
            return self.____standard_items____[item_id]
        except:
            return None
    
# -------------test
     
# data = {
#     "item_id": "E0001",
#     "item_type": 0,
#     "item_source": 0,
#     "item_name": "gold ring",
#     "item_image": "D://",
#     "description": "You can buy something with it.",
#     "price": 50,
#     "equipment_attr": {
#         "damage": 10,
#         "defense": 11,
#         "durability": 12
#     }
# }

# item_attr = ItemAttr()
# item_attr = ParseDict(data, item_attr)

# print(item_attr)
    
        

