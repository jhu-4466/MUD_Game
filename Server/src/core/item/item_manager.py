# -*- coding: utf-8 -*-
 
# -----------------------------
# Topic: item_manager.py
# Author: 
# Created: 2023/05/05
# Description: 
# History:
#    <autohr>    <version>    <time>        <desc>
#    liuyuqi      v0.5.0      2023/05/05   basic build
# -----------------------------



import random
import datetime

from core.item.item import Item


class ItemManager:
    """
    manages all item instances happening in the system to generate the unique guid and a timestamp.
    self.items = {item_id: {GUID: item, ...}, ...}
    
    Args:
        owner: the game world
        items: all the items in the world
    """
    item_counter: int = 0
    
    def __init__(self, owner):
        self.owner = owner
        self.items = {}

    def create_a_item(self, item_id, player_id) -> Item:
        
        """
        create a item according to the item_id and assign it to the player by player_id

        Args: 
            item_id: str
            player_id: str
        Return:
            item
        """   
        
        item_guid, item_datetime = self.generate_guid(item_id)  
        item_attr = self.owner.items_helper.find_a_item_attr(item_id)
        item = Item(item_guid, item_datetime, player_id, item_attr)

        if item_id not in self.items:
            self.items[item_id] = { item_guid: item}
        else: 
            self.items[item_id][item_guid] = item
        return item
    
    
    def generate_guid(self, item_id):
        '''
        to generate a unique GUID of item specified item_type.
        GUID Structure: timestamp-item_id-random-counter
        Example: 20230507174515-00001-1A783-00000001
          len          14        any     5      8
        
        '''
        item_timestamp = datetime.datetime.now().timestamp()
        item_random = random.randint(0, 0xFFFFF)
        dt = datetime.datetime.fromtimestamp(item_timestamp)
        
        item_datetime = dt.strftime('%Y%m%d%H%M%S')
        
        guid = item_datetime
        guid += '-{}'.format(item_id)
        guid += '-{:05X}'.format(item_random & 0xFFFFF)
        guid += '-{:08X}'.format(self.item_counter & 0xFFFFFFFF)
        self.item_counter += 1
        return guid, item_datetime
    
    def find_a_item(self, item_id, item_guid):
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

    def destroy_a_item(self, item_id, item_guid):
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

        
        

