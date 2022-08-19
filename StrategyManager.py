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
        "on_big_crunch",
        "reevalute"]

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
            if self.conditions_met(strategy):
                print(f"Current strategy is {strategy.name}")
                self.last_strategy = self.current_strategy
                return strategy

    def conditions_met(self, strategy : Strategy) -> bool:
        all_conditions_met = True
        for condition in strategy.conditions:
            if condition[0] == "MIN_IP_MULT_LEVEL":
                if not self.check_min_ip_mult_level(condition[1]):
                    all_conditions_met = False
            elif condition[0] == "MAX_IP":
                if not self.check_max_ip(condition[1]):
                    all_conditions_met = False
            elif condition[0] == "MIN_IP":
                if not self.check_min_ip(condition[1]):
                    all_conditions_met = False
            elif condition[0] == "INF_UPGRADE_PURCHASED":
                if not self.check_inf_upgrade_purchased(condition[1]):
                    all_conditions_met = False
            elif condition[0] == "CHALLENGE_COMPLETED":
                if not self.check_challenge_completed(condition[1]):
                    all_conditions_met = False
            elif condition[0] == "AUTOBUYER_INTERVALS_MAXED":
                if not self.check_autobuyer_intervals_maxed():
                    all_conditions_met = False
            elif condition[0] == "MIN_DIM_BOOST":
                if not self.check_min_dim_boost(condition[1]):
                    all_conditions_met = False

        return all_conditions_met


    def check_min_ip_mult_level(self, minimum):
        if self.game_instance.InfinityManager.x2_multi_level < minimum:
            return False
        else:
            return True

    def check_max_ip(self, maximum):
        if int(self.game_instance.driver.execute_script("return player.infinitied")) > maximum:
            return False
        else:
            return True

    def check_min_ip(self, minimum):
        if int(self.game_instance.driver.execute_script("return player.infinitied")) < minimum:
            return False
        else:
            return True

    def check_inf_upgrade_purchased(self, upgrade):
        if upgrade not in self.game_instance.InfinityManager.purchased_upgrades:
            return False
        else:
            return True

    def check_challenge_completed(self, challenge_id):
        if challenge_id not in self.game_instance.ChallengeManager.completed_challenges:
            return False
        else:
            return True

    def check_autobuyer_intervals_maxed(self):
        interval_set = set(self.game_instance.AutobuyerManager.intervals_maxed)
        if not (len(interval_set) == 1 and list(interval_set)[0] == True):
            return False
        else:
            return True

    def check_min_dim_boost(self, minimum):
        if self.game_instance.DimensionManager.get_dimension_boosts() < minimum:
            return False
        else:
            return True