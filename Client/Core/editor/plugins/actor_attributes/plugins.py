# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: actor information plugin
# Author: k14
# Created: 2023.04.10
# Description: actor information plugin
# History:
#    <autohr>    <version>    <time>        <desc>
#    k14         v0.1         2023/04/10    build the basic
# -----------------------------


from core.editor.apis.plugins import DockableLocationEnum, DockablePluginBase
from .widgets import ActorInformationWidget


class ActorInformation(DockablePluginBase):
    NAME = "actor_information"
    WIDGET_CLASS = ActorInformationWidget
    DOCK_LOCATION = DockableLocationEnum.LEFT
    
    def get_title(self):
        return "角色信息"