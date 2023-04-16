# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: test item data
# Author: m14 & lyq
# Created: 2023.04.16
# -----------------------------


from utils.proto.se_world_pb2 import ItemType, Item

items = {}

blue_steel = Item(
    item_id = "M0001",
    item_type = ItemType.MATERIAL,
    name = "蓝钢",
    description = "一种蓝色的钢铁，相对柔软",
    price = 50,
    hardness = 111,
    strength = 222,
    stiffness = 333,
)
items[blue_steel.item_id] = blue_steel