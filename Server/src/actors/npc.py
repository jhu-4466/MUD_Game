# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: actor npc
# Author: m14
# Created: 2023.04.22
# Description: create actor regularly
# History:
#       <autohr>       <version>      <time>        <desc>
#         m14           v0.5        2023/04/22      basic build simply
# -----------------------------


from core.actor.actor import Actor
from components.skills import Skills

from utils.proto.se_world_pb2 import ActorType, NPCAttr


class NPC(Actor):
    """

    a npc.

    Args:
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
    actor_type = ActorType.NPC
    actor_attr_type = NPCAttr

    def __init__(self, world):
        super().__init__(world)
    
    def on_initialize(self):
        # when connecting the database, it should complete a function like load_proto to change the attr during init.
        
        self.skills = Skills(self)
        self.add_component("skills", self.skills)


if __name__ == "__main__":
    from core.world.se_world import SEWorld
    
    npc = NPC(SEWorld("F:/CodeProjects/MUD_Game/Server/src/tests/skills.json"))
    print(npc.actor_attr)