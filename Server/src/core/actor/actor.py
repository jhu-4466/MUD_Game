# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: actor factory
# Author: yangchaohuan
# Created: 2023.04.14
# Description: create actor regularly
# History:
#       <author>       <version>      <time>        <desc>
#    yangchaohuan       v0.1        2023/04/14      basic build without protobuf
#         m14           v0.5        2023/04/15      basic build
# -----------------------------


from utils.proto.se_world_pb2 import ActorType, ActorAttr

import logging
import weakref
from google.protobuf.json_format import MessageToDict


class ActorMeta(type):
    types_dict = {}

    def __new__(mcs, clsname, bases, attrs):
        c = super(ActorMeta, mcs).__new__(mcs, clsname, bases, attrs)
        mcs.types_dict[c.actor_type] = c
        return c


class Actor(metaclass=ActorMeta):
    """

    the base actor.

    Args:
        metaclass (_type_, optional): _description_. Defaults to ActorMeta.
        actor_type: Actor Type in proto.
        actor_attr_type: Actor Attr in proto.
        activate_flag: the actor active state.
        id(str): unique actor id in database.
        name: actor name in database.
        ____world____: belongs to the world, if actor is disconnected, actor will be destoried after updating data in database.
        ____components_map____: all components belongs to the actor.
    """    
    actor_type = ActorType.ACTOR
    actor_attr_type = ActorAttr
    activate_flag: bool = False

    def __init__(self, world):
        self.id: str = 0
        self.name: str = ""
        self.____world____ = world
        self.____components_map____ = {}
        self.initialize()

    def initialize(self):
        self.actor_attr = self.actor_attr_type()
        self.on_initialize()

    def on_initialize(self):
        pass

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
        """

        update actor state and all components.
        
        Args:
            delta_time (int): an update circle.
        """    
        pass

    def get_component(self, comp_name):
        return self.____components_map____.get(comp_name)

    def add_component(self, comp_name, comp_inst, auto_activate=True):
        if comp_name in self.____components_map____:
            logging.error(f"Component {comp_name} already exists!")
            return
        comp_inst.owner = self
        self.____components_map____[comp_name] = comp_inst
        if auto_activate:
            comp_inst.activate()

    def remove_component(self, comp_name):
        if comp_name not in self.____components_map____:
            logging.info(f"Component {comp_name} not exists, ignore!")
            return
        comp_inst = self.____components_map____[comp_name]
        comp_inst.deactivate()
        comp_inst.owner = None
        del self.____components_map____[comp_name]

    def __getattr__(self, name):
        if name != "____components_map____":
            if hasattr(self, "____components_map____") and name in self.____components_map____:
                return self.____components_map____[name]
        raise AttributeError(
            f"{self.__class__.__name__} object has no attribute {name}")

    def __setattr__(self, name, value):
        if name != "____components_map____":
            if hasattr(self, "____components_map____") and name in self.____components_map____:
                self.____components_map____[name].load_proto(value)
                return
        object.__setattr__(self, name, value)

    def __repr__(self):
        return "%s(%s)(%d):\t| %s" % (
            self.name,
            ActorType.Name(self.actor_type),
            self.id,
            MessageToDict(self.actor_attr, including_default_value_fields=False,
                          preserving_proto_field_name=True)
        )


class ActorFactory(object):

    @classmethod
    def create_actor(cls, actor_type, world):
        import actors
        actor_cls = ActorMeta.types_dict.get(actor_type)
        actor = actor_cls(world=weakref.proxy(world))
        return actor