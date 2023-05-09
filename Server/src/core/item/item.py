# -*- coding: utf-8 -*-
 
# -----------------------------
# Topic: dataclass item
# Author: 
# Created: 2023/05/05
# Description: 
# History:
#    <author>    <version>    <time>        <desc>
#    liuyuqi      v0.5.0     2023/05/05   dataclass item
# -----------------------------


from utils.proto.se_world_pb2 import ItemAttr

from dataclasses import dataclass, field


@dataclass
class Item:
    """

    a Item dataclass, including some generated attr and orgin ItemAtrr
        
    """
    item_guid: str
    created_time: str
    assigned_id: str
    item_source: str
    item_attr: ItemAttr = field(default_factory=ItemAttr) 
    
    def __post_init__(self):        
        pass