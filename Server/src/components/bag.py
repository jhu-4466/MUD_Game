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

from tests.test_items_list import test_items


class Bag(Component):
    """

    the base component.
    
    Args:
        owner: an actor.
        ____items____: all items in a actor package.
    """
    component_name = "Bag"
    
    def __init__(self, owner):
        super().__init__(owner)
        
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
    
    def add_items(self, item_id: str, item_amount: int):
        """

        Put item into the bage

        Args:
            item_id (str): item id
            item_amount (int): item amount
        """
        if item_id not in self.____items____:
            self.____items____[item_id] = item_amount
        else:
            self.____items____[item_id] += item_amount
        
        # use database helper to commit the update
    
    def remove_items(self, item_id: str, item_amount: int):
        """

        Throw item from the bage

        Args:
            item_id (str): item id
            item_amount (int): item amount
        """
        curr_amount = self.____items____[item_id]
        
        if curr_amount <= item_amount:
            self.____items____.pop(item_id)
        else:
            self.____items____[item_id] -= item_amount
        
        # use database helper to commit the update

    def sell_item(self, item_id: str, item_amount: int):
        """

        sell item to the server

        Args:
            item_id (str): item id
            item_amount (int): item amount
        """
        curr_amount = self.____items____[item_id]
        
        if item_amount > curr_amount:
            return 
        
        self.owner.actor_attr.gold += test_items[item_id].price * item_amount
        self.remove_item(item_id, item_amount)
    
    def buy_item(self, item_id: str, item_amount: int):
        # may it should be written in the market component.
        pass

    def get_items(self):
        return self.____items____
    
    def get_a_item(self, item_id):
        return self.____items____[item_id]