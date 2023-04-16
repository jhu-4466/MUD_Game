# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: test data
# Author: m14 & lyq
# Created: 2023.04.16
# -----------------------------


from utils.proto.se_world_pb2 import PlayerAttr, ActorAttr, ActorType

player_attr = PlayerAttr(
    basic_attr=ActorAttr(actor_id='P000001', actor_name='取个名字好难', actor_type=ActorType.PLAYER),
    level=10,
    max_hp=1000,
    max_mp=500,
    cur_hp=800,
    cur_mp=300,
    physical_damage=100,
    magical_damage=50,
    physical_defence=80,
    magical_defence=60,
    exp=2000,
    gold=1000,
)