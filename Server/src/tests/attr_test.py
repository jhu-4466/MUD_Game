# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: test data
# Author: m14 & lyq
# Created: 2023.04.16
# -----------------------------


from utils.proto.se_world_pb2 import (
    PlayerAttr, ActorAttr, ActorType, NPCAttr, NumericAttr,
    LearnedSkill)

player_attr = PlayerAttr(
    basic_attr = ActorAttr(actor_id='P000001', actor_name='取个名字好难', actor_type=ActorType.PLAYER),
    numeric_attr = NumericAttr(
        level = 10,
        hp = 1000,
        mp = 500,
        physical_damage = 100,
        magical_damage = 50,
        physical_defence = 80,
        magical_defence = 60,
        exp = 2000
    ),
    gold = 1000,
    skill_points = 30,
    knew_npcids = ["NPC001"]
)

npc_attr = NPCAttr(
    basic_attr = ActorAttr(actor_id='NPC001', actor_name='许廷秀', actor_type=ActorType.NPC),
    numeric_attr = NumericAttr(
        level = 10,
        hp = 1000,
        mp = 500,
        physical_damage = 100,
        magical_damage = 50,
        physical_defence = 80,
        magical_defence = 60,
        exp = 2000
    ),
    learned_skills = [
        LearnedSkill(skill_id = "W001", curr_skill_level = 5)
    ],
    order_moves = ["attack", "W001"]
)