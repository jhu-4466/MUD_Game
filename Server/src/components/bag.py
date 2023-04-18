# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: bag component
# Author: m14
# Created: 2023.04.16
# Description: a bag component
# History:
#       <autohr>       <version>      <time>        <desc>
#         m14           v0.5        2023/04/16      basic build
# -----------------------------


from core.component.component import Component

from tests.test_items_list import items


class BagComponent(Component):
    """

    the base component.
    
    Args:
        owner_id(str): belongs to one actor.
        owner_attr: actor attr.
        items: all items in a actor package.
    """
    component_name = "Bag"
    
    def __init__(self, owner):
        super().__init__(owner)
        
        self.items = {}
    
    def tick(self, delta_time):
        pass
    
    def add_item(self, item_id: str, item_amount: int):
        """

        Put item into the bage

        Args:
            item_id (str): item id
            item_amount (int): item amount
        """
        if item_id not in self.items:
            self.items[item_id] = item_amount
        else:
            self.items[item_id] += item_amount
        
        # use database helper to commit the update
    
    def remove_item(self, item_id: str, item_amount: int):
        """

        Throw item from the bage

        Args:
            item_id (str): item id
            item_amount (int): item amount
        """
        curr_amount = self.items[item_id]
        
        if curr_amount <= item_amount:
            self.items.pop(item_id)
        else:
            self.items[item_id] -= item_amount
        
        # use database helper to commit the update

    def sell_item(self, item_id: str, item_amount: int):
        """

        sell item to the server

        Args:
            item_id (str): item id
            item_amount (int): item amount
        """
        curr_amount = self.items[item_id]
        
        if item_amount > curr_amount:
            return 
        
        self.owner.actor_attr.gold += items[item_id].price * item_amount
        self.remove_item(item_id, item_amount)
    
    def buy_item(self, item_id: str, item_amount: int):
        # may it should be written in the market component.
        pass

    def get_items(self):
        return self.items