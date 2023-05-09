# -*- coding: utf-8 -*-
 
# -----------------------------
# Topic: item.py
# Author: 
# Created: 2023/05/05
# Description: 
# History:
#    <autohr>    <version>    <time>        <desc>
#    liuyuqi      v0.5.0     2023/05/05   basic build
# -----------------------------


import sys
sys.path.append("../../")

from dataclasses import dataclass, field
from utils.proto.se_world_pb2 import ItemAttr


@dataclass
class Item:
    """

    a Item dataclass, including some generated attr and orgin ItemAtrr
        
    """
    item_guid: str
    item_datetime: str
    assign_id: str
    
    item_attr: ItemAttr = field(default_factory=ItemAttr) 
    
    def __post_init__(self):        
        pass
   
        

# test
# item1 = Item(0x01, ItemType.CONSUMABLE, ItemSource.SYSTEM, "gold", "The most expensive metal", 499.0, 4.0)
# print(item1)

# print(item1.guid)
# print(item2.guid)
# from collections import defaultdict

# dict1 = {"item_id": 1, "item_type": "a"}
# dict2 = {"item_id": 2, "item_type": "b", "item_price": 100}

# dict_test = {}
# dict_test["test"] = set("a")
# print(dict_test["test"])

# item2 = DynamicDataclass(dict2)ASDFz
# print("item2: ", item2)
    