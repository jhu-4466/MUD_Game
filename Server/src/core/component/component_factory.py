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


class ComponentMeta(type):
    types_dict = {}

    def __new__(mcs, clsname, bases, attrs):
        c = super().__new__(mcs, clsname, bases, attrs)
        mcs.types_dict[c.component_name] = c
        return c


class Component(metaclass=ComponentMeta):
    component_name: str = "BaseComponent"
    activate_flag: bool = False

    def __init__(self, owner_id):
        self.owner_id: int = owner_id

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
    
    def load_proto(self):
        pass


class ComponentFactory:
    @classmethod
    def create_component(cls, component_name: str):
        component_cls = ComponentMeta.types_dict.get(component_name)
        if component_cls is None:
            return None
        return component_cls()
