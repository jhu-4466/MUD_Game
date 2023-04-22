# -*- coding: utf-8 -*- #

# -----------------------------
# Topic: combat component
# Author: m14
# Created: 2023.04.21
# Description: a combat component
# History:
#       <autohr>       <version>      <time>        <desc>
#         m14           v0.5        2023/04/      basic build
# -----------------------------


from core.component.component import Component


class Combat(Component):
    """
    
    A component that represents a combat system with similar logic to 阴阳师.
    
    """
    component_name: str = "Combat"

    def __init__(self, team_a, team_b):
        self.on_initialize(team_a, team_b)

    def on_initialize(self, team_a, team_b, max_turn_time=100):
        """
        Initiates a combat between the specified players.

        Args:
            players (List[str]): a list of player IDs participating in the combat.
        """
        self.players = []
        self.players.extend(team_a)
        self.players.extend(team_b)
        self.max_turn_time = max_turn_time
        self.current_turn_order = self.get_next_player_turn_order()
        self.actions = []
        self.progress_bar = {player: 0 for player in players}
        
        self.on_combat_start()

    def on_combat_start(self):
        """
        Event triggered when a combat starts.
        """
        pass

    def on_combat_end(self):
        """
        Event triggered when a combat ends.
        """
        # TODO: Implement on_combat_end
        self.players = []
        self.current_turn_order = []
        self.actions = []
        self.progress_bar = {}


    def prompt_player_action(self, player_id: str):
        """
        Prompts the specified player to select an action.

        Args:
            player_id (str): the ID of the player being prompted.
        """
        # TODO: Implement prompt_player_action
        pass

    def apply_action(self, player_id: str, action: Dict[str, str]):
        """
        Applies the specified action to the specified player.

        Args:
            player_id (str): the ID of the player applying the action.
            action (Dict[str, str]): the action to apply.
        """
        # TODO: Implement apply_action

    def tick(self, delta_time: int):
        """
        Updates the combat state.

        Args:
            delta_time (int): the time since the last update.
        """
        # TODO: Implement tick

    def get_player_state(self, player_id: str) -> Dict[str, any]:
        """
        Returns the state of the specified player.

        Args:
            player_id (str): the ID of the player to get the state for.

        Returns:
            Dict[str, any]: a dictionary containing the state of the player.
        """
        # TODO: Implement get_player_state

    def get_combat_state(self) -> Dict[str, any]:
        """
        Returns the state of the current combat.

        Returns:
            Dict[str, any]: a dictionary containing the state of the current combat.
        """
        # TODO: Implement get_combat_state

    def is_combat_finished(self) -> bool:
        """
        Returns whether the current combat is finished or not.

        Returns:
            bool: True if the combat is finished, False otherwise.
        """
        # TODO: Implement is_combat_finished