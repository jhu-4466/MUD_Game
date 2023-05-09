# -*- coding: utf-8 -*-
 
# -----------------------------
# Topic: item_manager.py
# Author: 
# Created: 2023/05/05
# Description: 
# History:
#    <author>    <version>    <time>        <desc>
#    liuyuqi      v0.5.0      2023/05/05   create and destory item
# -----------------------------


import random
import datetime

from core.item.item import Item


class ItemManager:
    """
    manages all item instances happening in the system to generate the unique guid and a timestamp.
    self.items = {item_id: {GUID: item, ...}, ...}
    
    Attributes:
        owner: the game world
        items: all the items in the world
    """
    def __init__(self, owner):
        self.owner = owner

        self.items = {}

    def create_a_item(self, item_id: str, player_id: str, source_id: str) -> Item:
        """
        create a item according to the item_id and assign it to the player by player_id

        Args: 
            item_id: str
            player_id: str
            source_id: str
        Return:
            item: dataclass
        """   
        item_guid, created_time = self._generate_guid(item_id)
        item_attr = self.owner.items_helper.find_a_item(item_id)
        
        item = Item(item_guid, created_time, player_id, source_id, item_attr)

        if item_id not in self.items:
            self.items[item_id] = {item_guid: item}
        else: 
            self.items[item_id][item_guid] = item
        return item
    
    def _generate_guid(self, item_id: str):
        """
        to generate a unique GUID of item specified item_type.
        GUID Structure: timestamp-item_id-random-counter
        Example: 20230507174515-00001-1A783-00000001
          len          14        any     5      8
          
        Args:
            item_id: str
        Return:
            guid: str
            created_time: str
        """
        created_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        guid = created_time
        guid += '-{}'.format(item_id)
        guid += '-{:05X}'.format(random.randint(0, 0xFFFFF) & 0xFFFFF)
        guid += '-{:08X}'.format(len(self.items[item_id]) + 1 if item_id in self.items else 1
                                 & 0xFFFFFFFF)
        return guid, created_time
    
    def destroy_a_item(self, item_id: str, item_guid: str):
        """
        Destory a item instance from the items dictionary.

        Args:
            item_id, item_guid
        Return:
            True or False
        """
        if item_id in self.items:
            if item_guid in self.items[item_id]:
                del self.items[item_id][item_guid]
                return True
        return False
    
    def find_a_item(self, item_id: str, item_guid: str):
        """
        Find a item assigned with item_id and item_guid

        Args: 
            item_id: str
            item_guid: str
        Return:
            item
        """
        try:
            return self.items[item_id][item_guid]
        except:
            return None
    
    def find_a_price(self, item_id: str, item_guid: str):
        """
        Find the price of item  with item_id and item_guid

        Args: 
            item_id: str
            item_guid: str
        Return:
            price: int
        """
        try:
            return self.items[item_id][item_guid].item_attr.price
        except:
            return None
        

    

        
        

