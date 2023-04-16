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


class BagComponent(Component):
    def __init__(self, owner_id, world):
        super().__init__(owner_id, world)
        
        self.items = {}
    
    def tick(self, delta_time):
        pass
    
    def add_item(self, item_id: str, item_count: int):
        if item_id not in self.items:
            self.items[item_id] = item_count
        else:
            self.items[item_id] += item_count
        
        # use database helper to commit the update
    
    def remove_item(self, item_id: str, item_count: int):
        curr_count = self.items[item_id]
        
        if curr_count <= item_count:
            self.items.pop(item_id)
        else:
            self.items[item_id] -= item_count
        
        # use database helper to commit the update

    def get_items(self):
        return self.items