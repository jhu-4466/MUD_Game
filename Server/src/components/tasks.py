# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: task component
# Author: m14
# Created: 2023.04.19
# Description: create factory regularly
# History:
#       <author>       <version>      <time>        <desc>
#         m14           v0.5        2023/04/21      basic build
# -----------------------------
import sys
sys.path.append("../")


from core.component.component import Component

from utils.proto.se_world_pb2 import (
    TaskTriggerConditionsType, TaskRewardType, RunningTask,
    TaskProcessType, TaskCombatState, TaskProcessType)


class Tasks(Component):
    """
    
    a task component.

    Args:
        standby_tasks (List[str]): holds IDS in standby tasks list.
        running_tasks (List[RunningTask]): holds RunningTask in running tasks list.
        finished_tasks (List[str]): holds IDS in finished tasks list.
    """    
    component_name = "Tasks"

    def __init__(self, owner):
        super().__init__(owner)
        
        self.standby_tasks = self.owner.actor_attr.standby_tasks
        self.running_tasks = self.owner.actor_attr.running_tasks
        self.finished_tasks = self.owner.actor_attr.finished_tasks
        
        self.tasks_helper = self.owner.world.tasks_helper

    def load_proto(self, value):
        """
        
        update attr from proto data.

        Args:
            value (ActorAttr): actor attr.
        """     
        pass

    def tick(self, delta_time=None):
        """
        
        update three task lists.
        
        """        
        standard_tasks = self.tasks_helper.standard_tasks
        
        for task_id, task_attr in standard_tasks.items():
            if task_id in self.finished_tasks:
                continue
            
            task_state = False
            for tt in task_attr.trigger_conditions:
                if tt.tc_type == TaskTriggerConditionsType.LEVEL and \
                    self.owner.actor_attr.numeric_attr.level >= int(tt.tc_content):
                    task_state = True
                    continue
                elif tt.tc_type == TaskTriggerConditionsType.PRETASK and \
                    tt.tc_content in self.finished_tasks:
                    task_state = True
                    continue
                else:
                    task_state = False
                    break
            if task_state and task_id not in self.standby_tasks and \
                task_id not in self._find_running_tasks_ids() and \
                task_id not in self.finished_tasks:
                self.standby_tasks.append(task_id)

    def trigger_a_task(self, task_id, npc_id):
        """
        
        trigger a task

        Args:
            task_id (str): task id
            npc_id (str): task assigned id, and one task is only associated with a npc.
        Returns:
            bool: whether trigger successly
        """        
        task_attr = self.tasks_helper.find_a_task(task_id)
        if task_id not in self.standby_tasks or task_attr.assigned_npcid != npc_id:
            return False
        
        self.standby_tasks.remove(task_id)
        running_task = RunningTask(
            task_id=task_id, curr_index=0, assigned_npcid=npc_id, combat_state=TaskCombatState.UNKNOWN)
        self.running_tasks.append(running_task)
        
        return True
    
    def task_next_step(self, task_id, npc_id):
        """
        
        go to a next step of the task dialogs

        Args:
            task_id (str): task id
            npc_id (str): task assigned id, and one task is only associated with a npc.
        Returns:
            bool: whether next successly
        """  
        running_tasks_ids = self._find_running_tasks_ids()
        if task_id not in running_tasks_ids:
            return False
        running_task = self._find_a_running_task(task_id)
        if running_task.assigned_npcid != npc_id:
            return False
        
        running_task_attr = self.tasks_helper.find_a_task(running_task.task_id)
        curr_task_process = running_task_attr.task_process[running_task.curr_index]
        
        next_flag = False
        if curr_task_process.tp_type == TaskProcessType.DIALOGS:
            next_flag = True
        elif curr_task_process.tp_type == TaskProcessType.COMBAT:
            next_flag = self._check_combat_state(running_task, curr_task_process)
        elif curr_task_process.tp_type == TaskProcessType.ITEM:
            next_flag = self._check_material_items(curr_task_process)
        elif curr_task_process.tp_type == TaskProcessType.SKILLS:
            # check skills amount
            next_flag = self._check_skills_amount(curr_task_process.tp_content)
        elif curr_task_process.tp_type == TaskProcessType.SKILLLEVELS:
            # check the highest skill level
            next_flag = self._check_skill_level(curr_task_process.tp_content)
        elif curr_task_process.tp_type == TaskProcessType.LEVELS:
            next_flag = self._check_player_level(curr_task_process.tp_content)
        elif curr_task_process.tp_type == TaskProcessType.FIND:
            next_flag = self._check_knew_ids(running_task, curr_task_process.tp_content)
        if not next_flag:
            return False
        
        for reward in curr_task_process.tp_reward:
            self._distribute_a_reward(reward)
        running_task.curr_index += 1
        if running_task.curr_index == len(running_task_attr.task_process):
            self._finish_a_task(task_id, npc_id)
        return True
    
    def _check_combat_state(self, running_task, curr_task_process):
        if running_task.combat_state == TaskCombatState.WIN:
            return True
        else:
            self.owner.world.add_a_combat(
                self.owner.id, running_task.assigned_npcid, curr_task_process.npc_combatplan_index, running_task)
        return False

    def _check_material_items(self, curr_task_process):
        bag = self.owner.bag
        items = bag.get_items()
        
        for item_id, item_amount in zip(curr_task_process.tp_content, curr_task_process.items_amount):
            if item_id not in items:
                return False
            if item_amount > items[item_id]:
                return False
        for item_id, item_amount in zip(curr_task_process.tp_content, curr_task_process.items_amount):
            bag.remove_items(item_id, item_amount)

        return True

    def _check_skills_amount(self, skills_amount):
        skills = self.owner.skills
        
        return len(skills.learned_skills) >= skills_amount
    
    def _check_skill_level(self, skill_level):
        skills = self.owner.skills
        
        return skill_level <= skills.find_highest_skill_level()
    
    def _check_player_level(self, player_level):
        return player_level <= self.owner.actor_attr.numeric_attr.level
    
    def _check_knew_ids(self, running_task, npc_id):
        knew_ids = self.owner.actor_attr.knew_npcids
        if npc_id not in knew_ids:
            return False
        
        running_task.assigned_npcid = npc_id
        return True
    
    def _finish_a_task(self, task_id, npc_id):
        """
        
        check whether finish a task.

        Args:
            task_id (str): task id
            npc_id (str): task assigned id, and one task is only associated with a npc.
        Returns:
            bool: whether finish successly
        """  
        task_attr = self.tasks_helper.find_a_task(task_id)
        if npc_id not in self.owner.actor_attr.knew_npcids:
            return False
        
        running_task = self._find_a_running_task(task_id)
        self.running_tasks.remove(running_task)
        self.finished_tasks.append(task_id)
        
        for reward in task_attr.task_reward:
            self._distribute_a_reward(reward)
    
        return True

    def _distribute_a_reward(self, reward):
        """
        
        distribute a reward one time.
        
        Returns:
            reward (TaskReward): reward content.
        """
        if reward.tr_type == TaskRewardType.SKILLPOINTS:
            self.owner.actor_attr.skill_points += int(reward.tr_content)
        elif reward.tr_type == TaskRewardType.EXP:
            self.owner.actor_attr.exp += int(reward.tr_content)
        elif reward.tr_type == TaskRewardType.GOLD:
            self.owner.actor_attr.gold += int(reward.tr_content)
        elif reward.tr_type == TaskRewardType.ITEMS:
            self.owner.bag.add_items(reward.tr_content, reward.tr_amount)
        elif reward.tr_type == TaskRewardType.NEWNPC:
            self.owner.actor_attr.knew_npcids.append(reward.tr_content)

    def _find_running_tasks_ids(self):
        """
        
        find actor's running tasks ids.
        
        Returns:
            ids: actor's learned tasks ids.
        """
        ids = set()
        for task in self.running_tasks:
            ids.add(task.task_id)
        return ids
    
    def _find_a_running_task(self, task_id):
        """
        
        find a actor's running task.

        Returns:
            task: a message RunningTask
        """
        for task in self.running_tasks:
            if task.task_id == task_id:
                return task

    def __repr__(self):
        output = "可接技能："
        for e in self.standby_tasks:
            output += (e + "、")
        output += "\n正在进行任务： "
        for e in self.running_tasks:
            output += (e.task_id + f'({e.curr_index})' + "、")
        output += "\n已完成任务： "
        for e in self.finished_tasks:
            output += (e + "、")
        
        return output


if __name__ == "__main__":
    from utils.proto.se_world_pb2 import PlayerAttr
    from components.bag import Bag
    from components.skills import Skills
    from core.world.se_world import SEWorld
    from core.actor.actor import Actor
    
    class Player(Actor):
        def __init__(self, owner):
            super().__init__(owner)
            
            self.actor_attr = PlayerAttr()
            
            self.actor_attr.basic_attr.actor_id = "P001"
            self.actor_attr.numeric_attr.level = 0
            self.actor_attr.knew_npcids.append("NPC001")
            
            self.bag = Bag(self)
            self.tasks = Tasks(self)
            self.skills = Skills(self)
    
    player = Player(SEWorld(
        skill_file="F:/CodeProjects/MUD_Game/Server/src/tests/skills.json",
        task_file="F:/CodeProjects/MUD_Game/Server/src/tests/tasks.json"))
    player.tasks.tick()
    
    curr_task_id = ""
    try:
        while True:
            s = input("请输入你的操作：").split(' ')
            if s[0] == "trigger":
                print(player.tasks.trigger_a_task(s[1], s[2]))
                print(player.tasks.helper.find_a_task(s[1]).task_dialogs[
                    player.tasks._find_a_running_task(s[1]).curr_index])
            elif s[0] == "next":
                print(player.tasks.task_next_step(s[1], s[2]))
                print(player.tasks.helper.find_a_task(s[1]).task_dialogs[
                    player.tasks._find_a_running_task(s[1]).curr_index])
            elif s[0] == "finish":
                print(player.tasks.finish_a_task(s[1], s[2]))
            elif s[0] == "show":
                print(player.tasks)
                print(player.actor_attr)
            elif s[0] == "learn":
                print(player.skills.learn_skill(s[1]))
            else:
                print("please check your order!")
            player.tasks.tick()
    except KeyboardInterrupt:
        player.tasks.tick()