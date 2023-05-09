# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: bag component
# Author: m14
# Created: 2023.04.16
# Description: a bag component
# History:
#       <autohr>       <version>      <time>        <desc>
#         m14           v0.5        2023/04/16      basic build
#         liuyuqi       v0.5.0      2023/05/08      adjust
# -----------------------------


from core.component.component import Component
from core.item.item_manager import ItemManager
class Bag(Component):
    """

    the base component.
    
    Args:
        owner: an actor.
        ____items____: all items in a actor package, {item_id: set(item_guid), ...}.
    """
    component_name = "Bag"
    
    def __init__(self, owner):
        super().__init__(owner)
        self.items_helper = self.owner.world.items_helper
        
        self.____items____ = {}
    
    @property
    def items(self):
        return self.____items____
    
    def load_proto(self, value):
        """
        
        update attr from proto data.

        Args:
            value (ActorAttr): actor attr.
        """     
        pass
    
    
    def add_a_item(self, item_id: str, item_guid: str):
        """

        Put item into the bage

        Args:
            item_id (str): item id
            item_amount (int): item amount
        """
        if item_id not in self.____items____:
            self.____items____[item_id] = set()
            self.____items____[item_id].add(item_guid)
            return
        self.____items____[item_id].add(item_guid)
        
        
    
    def remove_items(self, item_id: str, item_amount: int):
        """

        Throw item from the bage

        Args:
            item_id (str): item id
            item_amount (int): item amount
        """
        if item_id not in self.____items____:
            return False
        
        curr_amount = len(self.____items____[item_id])
        if curr_amount < item_amount:
            return False
        
        for i in range(item_amount):
            del_item_guid = self.____items____[item_id].pop()
            self.owner.world.item_manager.destroy_a_item(item_id, del_item_guid)
        if not self.____items____[item_id]:
            del self.____items____[item_id]
        return True
                
        
        # use database helper to commit the update

    def sell_items(self, item_id: str, item_amount: int):
        """

        sell item to the server

        Args:
            item_id (str): item id
            item_amount (int): item amount
        """
        curr_amount = len(self.____items____[item_id])
        
        if item_amount > curr_amount:
            return False
        
        # Sell it but don't destroy it
        for i in range(item_amount):
            self.____items____[item_id].pop()
            
            # NEED TO DO: 
            #       modify the assign_id according the guid
        self.owner.actor_attr.gold += self.items_helper.find_a_price(item_id) * item_amount
        
    def buy_item(self, item_id: int, item_amount: int):
        # may it should be written in the market component.
        pass

    def get_items(self):
        """

        get all the items in bag

        Return:
            a dict, {item_id: [item1, item2,...], ...}

        """
        items = {}
        for item_id in self.____items____:
            items[item_id] = []
            for item_guid in self.____items____[item_id]:
                items[item_id].append(self.get_a_item(item_id, item_guid))
        return items
    
    def get_a_item(self, item_id, item_guid):
        item = self.owner.world.item_manager.find_a_item(item_id, item_guid)
        return item
    
    def get_item_amount(self, item_id):
        try: 
            return len(self.____items____[item_id])
        except:
            return None 