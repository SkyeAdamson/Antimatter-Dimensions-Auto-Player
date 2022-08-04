import json
from Strategy import Strategy

class StrategyManager:

    all_supported_keys = [
        "active_challenge",
        "autobuyers_enabled",
        "autobuyers_priority",
        "auto_dimboost_max_8ths",
        "break_infinity",
        "big_crunch_amount",
        "galaxies_to_always_dimboost",
        "max_galaxies",
        "on_big_crunch"]

    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.strategies = []
        self.current_strategy = None
        self.last_strategy = None

    def construct_strategies_from_json(self):
        with open('Strategies.json', 'r') as json_file:
            json_data = json.load(json_file)
            for json_strategy in json_data["strategies"]:
                name = json_strategy["strategy_name"]
                priorities_list = []
                for priority in json_strategy["priorities"]:
                    for key, value in priority.items():
                        priorities_list.append((key, value))
                conditions_list = []
                for condition in json_strategy["conditions"]:
                    for key, value in condition.items():
                        conditions_list.append((key, value))

                modifiers = dict.fromkeys(self.all_supported_keys, None)
                extra_keys = [key for key in list(json_strategy.keys()) if key not in ["strategy_name", "priorities", "conditions"]]
                
                for key in extra_keys:
                    modifiers[key] = json_strategy[key]

                strategy_obj = Strategy(name, priorities_list, conditions_list, modifiers)
                self.strategies.append(strategy_obj)

    def perform_strategy_setup(self):
        """
        Sets up the game with whatever requirements (if any) a strategy needs
        """
        if self.current_strategy.active_challenge != None:
            self.game_instance.ChallengeManager.start_challenge(self.current_strategy.active_challenge)

        if self.current_strategy.autobuyers_priority == "default":
            for idx in range(1, 10):
                self.game_instance.AutobuyerManager.set_autobuyer_priority(idx, idx)

        if self.current_strategy.autobuyers_enabled:
            self.game_instance.AutobuyerManager.enable_autobuyers()

        if not self.current_strategy.auto_dimboost_max_8ths == None:
            self.game_instance.AutobuyerManager.set_auto_dim_max_8ths(self.current_strategy.auto_dimboost_max_8ths)

        if self.current_strategy.break_infinity:
            self.game_instance.InfinityManager.enable_break_infinity()
            if self.current_strategy.big_crunch_amount != None:
                self.game_instance.AutobuyerManager.set_big_crunch_amount(self.current_strategy.big_crunch_amount)

        if self.current_strategy.galaxies_to_always_dimboost != None:
            self.game_instance.AutobuyerManager.set_galaxies_to_dim_boost(self.current_strategy.galaxies_to_always_dimboost)

        if self.current_strategy.max_galaxies != None:
            self.game_instance.AutobuyerManager.set_max_galaxies(self.current_strategy.max_galaxies)

    def choose_current_strategy(self) -> Strategy:
        """
        Returns the first strategy matching all conditions
        """
        for strategy in self.strategies:
            if strategy.conditions_met(self.game_instance):
                print(f"Current strategy is {strategy.name}")
                self.last_strategy = self.current_strategy
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