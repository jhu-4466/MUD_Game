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
from components.bag import Bag
from components.skills import Skills
from components.tasks import Tasks

from utils.proto.se_world_pb2 import ActorType, PlayerAttr


class Player(Actor):
    """

    the base actor.

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
    actor_type = ActorType.PLAYER
    actor_attr_type = PlayerAttr

    def __init__(self, world):
        super().__init__(world)

    def on_initialize(self):
        # test attr
        self.actor_attr = player_attr
        
        self.bag = Bag(self)
        self.add_component("bag", self.bag)
        self.skills = Skills(self)
        self.add_component("skills", self.skills)
        self.tasks = Tasks(self)
        self.add_component("tasks", self.tasks)

    def tick(self, delta_time):
        """

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
    
    def learn_skill(self, target_id: str):
        return self.skills.learn_skill(target_id)
    
    def remove_skill(self, target_id: str):
        return self.skills.remove_skill(target_id)
    
    def upgrade_skill_levels(self, target_id, upgrade_count):
        return self.skills.upgrade_skill_levels(target_id, upgrade_count)

    def demote_skill_levels(self, target_id, demote_count):
        return self.skills.demote_skill_levels(target_id, demote_count)
    
    def reset_skills(self):
        return self.skills.reset_skills()
    
    def trigger_a_task(self, task_id, npc_id):
        return self.tasks.trigger_a_task(task_id, npc_id)
    
    def task_next_step(self, task_id, npc_id):
        return self.tasks.task_next_step(task_id, npc_id)
    
    def finish_a_task(self, task_id, npc_id):
        return self.tasks.finish_a_task(task_id, npc_id)

if __name__ == "__main__":
    from core.world.se_world import SEWorld
    from core.actor.actor import ActorFactory
    player = ActorFactory.create_actor(ActorType.PLAYER, 
                                       SEWorld("F:/CodeProjects/MUD_Game/Server/src/tests/skills.json"))
    # player.add_item("M0001", 2)
    # print(player.bag.items)
    
    # print(player.learn_skill("W001"))
    # print(player.learn_skill("W004"))
    # print(player.learn_skill("W002"))
    # print(player.learn_skill("W004"))
    # print(player.upgrade_skill_levels("W004", 11))
    # print(player.demote_skill_levels("W002", 1))
    # print(player.skills)
    # print("剩余技能点: ", player.actor_attr.skill_points)
    # print(player.remove_skill("W002"))
    # print(player.skills)
    # print("剩余技能点: ", player.actor_attr.skill_points)
    # print(player.reset_skills())
    # print(player.skills)
    # print("剩余技能点: ", player.actor_attr.skill_points)
    
    # try:
    #     while True:
    #         player.tick(0.5)
    # except KeyboardInterrupt:
    #     sys.exit()