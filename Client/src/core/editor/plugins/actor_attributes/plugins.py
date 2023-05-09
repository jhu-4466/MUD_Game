# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: actor information plugin
# Author: m14
# Created: 2023.04.10
# Description: actor information plugin
# History:
#    <author>    <version>    <time>        <desc>
#    m14         v0.1         2023/04/10    build the basic
# -----------------------------


from core.editor.apis.plugins import DockableLocationEnum, DockablePluginBase
from .widgets import ActorAttributesWidget


class ActorAttributes(DockablePluginBase):
    NAME = "actor_attributes"
    WIDGET_CLASS = ActorAttributesWidget
    DOCK_LOCATION = DockableLocationEnum.LEFT
    
    def get_title(self):
        return "角色属性"