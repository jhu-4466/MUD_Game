# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: component factory
# Author: m14
# Created: 2023.04.15
# Description: create factory regularly
# History:
#       <autohr>       <version>      <time>        <desc>
#         m14           v0.5        2023/04/15      basic build
# -----------------------------


from core.world.se_world import SEWorld


class Component:
    """_summary_

    the base component.
    
    Args:
        component_name(int): component name.
        activate_flag(bool): component active state.
        owner(str): belongs to one actor.
    """
    component_name: str = "BaseComponent"
    activate_flag: bool = False

    def __init__(self, owner):
        self.owner = owner

    @property
    def world(self):
        return self.____world____

    @world.setter
    def world(self, value):
        self.____world____ = value

    def activate(self):
        if self.activate_flag:
            return
        self.activate_flag = True
        self.on_activated()

    def deactivate(self):
        if not self.activate_flag:
            return
        self.activate_flag = False
        self.on_deactivated()

    def is_activate(self):
        return self.activate_flag

    def on_activated(self):
        pass

    def on_deactivated(self):
        pass

    def tick(self, delta_time):
        """_summary_

        update component state.
        
        Args:
            delta_time (int): an update circle.
        """        
        pass
    
    def load_proto(self, value):
        pass