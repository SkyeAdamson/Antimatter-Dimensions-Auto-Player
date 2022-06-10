import json
from Strategy import Strategy

class StrategyManager:

    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.strategies = []
        self.current_strategy = None

    def construct_strategies_from_json(self):
        with open('Strategies.json', 'r') as json_file:
            json_data = json.load(json_file)
            for json_strategy in json_data["strategies"]:
                name = json_strategy["strategy_name"]
                challenge_id = json_strategy["active_challenge"]
                priorities_list = []
                for priority in json_strategy["priorities"]:
                    for key, value in priority.items():
                        priorities_list.append((key, value))
                strategy_obj = Strategy(name, priorities_list, challenge_id, [])
                self.strategies.append(strategy_obj)

    def choose_current_strategy(self) -> Strategy:
        """
        Returns the first strategy matching all conditions
        """
        for strategy in reversed(self.strategies):
            if strategy.conditions_met(self.game_instance):
                return strategy

    def pre_infinity_strategy(self):
        if self.game_instance.DimensionManager.get_galaxy_count() < 2:
            self.game_instance.DimensionManager.purchase_upgrade("secondSoftReset")
        if self.game_instance.DimensionManager.get_dimension_boosts() < 16:
            self.game_instance.DimensionManager.purchase_upgrade("softReset")
        self.game_instance.DimensionManager.purchase_sacrifice()
        self.game_instance.DimensionManager.purchase_upgrade("tickSpeedMax")
        for d_id in range(8, 0, -1):
            self.game_instance.DimensionManager.purchase_upgrade(f"M{d_id}")
        for d_id in range(8, 0, -1):
            self.game_instance.DimensionManager.purchase_upgrade(f"B{d_id}")