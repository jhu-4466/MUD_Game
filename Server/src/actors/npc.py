# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: actor npc
# Author: m14
# Created: 2023.04.22
# Description: create actor regularly
# History:
#       <author>       <version>      <time>        <desc>
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
        self.skills = Skills(self)
        self.add_component("skills", self.skills)
    
    def load_proto(self, player, npc_id, combatplan_index):
        self.____player____ = player
        
        self.id = npc_id + player.replace('P', '')
        self.npc_id = npc_id
        
        npc_attr = self.world.npcs_helper.find_a_npc(self.npc_id)
        self.actor_attr.CopyFrom(npc_attr)
        combat_plan = npc_attr.combat_plans[combatplan_index]
        self.actor_attr.numeric_attr.CopyFrom(combat_plan.numeric_attr)
        self.actor_attr.learned_skills.extend(combat_plan.learned_skills)
        self.actor_attr.combat_orders.extend(combat_plan.combat_orders)
        self.actor_attr.combat_order_index = combat_plan.combat_order_index
        
        self.skills = self.actor_attr
    
    @property
    def player(self):
        return self.____player____


if __name__ == "__main__":
    from core.world.se_world import SEWorld
    
    npc = NPC(SEWorld(skill_file="F:/CodeProjects/MUD_Game/Server/src/tests/skills.json",
                      task_file="F:/CodeProjects/MUD_Game/Server/src/tests/tasks.json",
                      npc_file="F:/CodeProjects/MUD_Game/Server/src/tests/npcs.json"))
    npc.load_proto('P000001', "NPC003", 0)