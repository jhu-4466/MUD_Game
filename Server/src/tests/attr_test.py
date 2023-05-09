# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: test data
# Author: m14 & lyq
# Created: 2023.04.16
# -----------------------------


from utils.proto.se_world_pb2 import (
    PlayerAttr, ActorAttr, ActorType, NumericAttr,
    LearnedSkill)

player1_attr = PlayerAttr(
    basic_attr = ActorAttr(actor_id='P000001', actor_name='取个名字好难', actor_type=ActorType.PLAYER),
    numeric_attr = NumericAttr(
        level = 10,
        hp = 200,
        mp = 500,
        physical_damage = 100,
        magical_damage = 50,
        physical_defence = 80,
        magical_defence = 60,
        speed = 20,
    ),
    learned_skills = [
        LearnedSkill(skill_id = "S000", curr_skill_level = 1),
        LearnedSkill(skill_id = "W003", curr_skill_level = 1)
    ],
    exp = 2000,
    gold = 1000,
    skill_points = 30,
    knew_npcids = ["NPC003"]
)


player2_attr = PlayerAttr(
    basic_attr = ActorAttr(actor_id='P000002', actor_name='取个名字不难', actor_type=ActorType.PLAYER),
    numeric_attr = NumericAttr(
        level = 10,
        hp = 200,
        mp = 500,
        physical_damage = 100,
        magical_damage = 50,
        physical_defence = 80,
        magical_defence = 60,
        speed = 20,
    ),
    learned_skills = [
        LearnedSkill(skill_id = "S000", curr_skill_level = 1),
        LearnedSkill(skill_id = "W003", curr_skill_level = 1)
    ],
    exp = 2000,
    gold = 1000,
    skill_points = 30,
    knew_npcids = ["NPC003"]
)