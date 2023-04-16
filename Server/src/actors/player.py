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
import sys
sys.path.append("../")


from core.actor.actor import Actor
from components.bag import BagComponent

from utils.proto.se_world_pb2 import ActorType, PlayerAttr


class Player(Actor):
    actor_type = ActorType.PLAYER
    actor_attr_type = PlayerAttr

    def __init__(self, world):
        super().__init__(world)

    def on_initialize(self):
        # test attr
        self.actor_attr.basic_attr.actor_id = "1"
        
        self.bag = BagComponent(self.actor_attr.basic_attr.actor_id, self.world)
        self.add_component("bag", self.bag)

    def tick(self):
        pass

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
    print(player.get_items())