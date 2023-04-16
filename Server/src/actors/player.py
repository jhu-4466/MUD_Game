# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: actor player
# Author: m14
# Created: 2023.04.14
# Description: create actor regularly
# History:
#       <autohr>       <version>      <time>        <desc>
#         m14           v0.5        2023/04/15      basic build simply
# -----------------------------

# test import
import sys
sys.path.append("../")
from tests.player_attr_test import player_attr


from core.actor.actor import Actor
from components.bag import BagComponent

from utils.proto.se_world_pb2 import ActorType, PlayerAttr


class Player(Actor):
    """_summary_

    the base actor.

    Attributes:
        metaclass (_type_, optional): _description_. Defaults to ActorMeta.
        actor_type: Actor Type in proto.
        actor_attr: Actor Attr in proto.
        actor_attr_type: new a actor attr by proto.
        activate_flag: the actor active state.
        id(str): unique actor id in database.
        name: actor name in database.
        ____world____: belongs to the world, if actor is disconnected, actor will be destoried after updating data in database.
        ____components_map____: all components belongs to the actor.
    """  
    actor_type = ActorType.PLAYER
    actor_attr_type = PlayerAttr

    def __init__(self, world):
        super().__init__(world)

    def on_initialize(self):
        # test attr
        self.actor_attr = player_attr
        
        self.bag = BagComponent(self.actor_attr.basic_attr.actor_id, self.world)
        self.add_component("bag", self.bag)

    def tick(self, delta_time):
        """_summary_

        tick self state and all components.

        Args:
            delta_time (_type_): _description_
        """
        # self attr
        
        for component in self.____components_map____.values():
            component.tick(delta_time)

    def add_item(self, item_id: int, count: int):
        self.bag.add_item(item_id, count)

    def remove_item(self, item_id: int, count: int):
        self.bag.remove_item(item_id, count)

    def get_items(self):
        return self.bag.get_items()


if __name__ == "__main__":
    from core.world.se_world import SEWorld
    from core.actor.actor import ActorFactory
    player = ActorFactory.create_actor(ActorType.PLAYER, SEWorld())
    player.add_item(1, 1)
    
    try:
        while True:
            player.tick(0.5)
    except KeyboardInterrupt:
        sys.exit()