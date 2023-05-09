# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: task tree helper
# Author: m14
# Created: 2023.04.19
# Description: task tree helper
# History:
# <autohr>       <version>      <time>        <desc>
#   m14           v0.5        2023/04/20      basic build
# -----------------------------


from utils.proto.se_world_pb2 import TaskAttr

import json
from google.protobuf.json_format import ParseDict


class TasksHelper:
    """
    
    maintains the standard tasks.
    
    Args:
        owner: the game world
        file_path: tasks data file.
        ____standard_tasks____: standard all tasks.
    """
    def __init__(self, owner, file_path: str):
        self.owner = owner
        self.file_path = file_path
        
        self.initialize()
    
    def initialize(self):
        self.____standard_tasks____ = {}
        
        self.on_initialize()
    
    def on_initialize(self):
        self.load_json()

    @property
    def standard_tasks(self):
        return self.____standard_tasks____

    def load_json(self):
        """
        
        load tasks data from json.
        
        """
        tasks_json = open(self.file_path, 'r', encoding="utf-8")
        tasks_data = json.load(tasks_json)

        for task in tasks_data:
            task_attr = ParseDict(task, TaskAttr())
            self.____standard_tasks____[task_attr.task_id] = task_attr
        
        tasks_json.close()
        
    def find_a_task(self, task_id):
        """

        by task id, finds the task attr in stanard task

        Args:
            task_id (str): the id of a target task.
        Returns:
            TaskAttr: task proto message 
        """
        try:
            return self.____standard_tasks____[task_id]
        except:
            return None


if __name__ == "__main__":
    a = TasksHelper("D:/liuyuqi/SkyEye/MUD_Game/Server/src/tests/tasks.json")
    
    print(a.standard_tasks)