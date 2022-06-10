class Strategy:

    def __init__(self, name, priority_list, strategy_challenge, conditions):
        self.name = name
        self.priority_list = priority_list
        self.strategy_challenge = strategy_challenge
        self.conditions = conditions

    def conditions_met(self, game_instance):
        return True

    def execute_strategy(self, game_instance):
        for priority in self.priority_list:
            if priority[0] == "BIG_CRUNCH":
                if game_instance.InfinityManager.big_crunch():
                    game_instance.InfinityManager.buy_available_upgrades()
                    game_instance.BrowserManager.load_dimensions()
                    game_instance.StrategyManager.current_strategy = game_instance.StrategyManager.choose_current_strategy()
                    break
            elif priority[0] == "ANTIMATTER_GALAXY":
                if priority[1] != None:
                    if game_instance.DimensionManager.get_galaxy_count() < priority[1]:
                        game_instance.DimensionManager.purchase_upgrade("secondSoftReset")
                else:
                    game_instance.DimensionManager.purchase_upgrade("secondSoftReset")
            elif priority[0] == "DIMENSION_BOOST":
                if priority[1] != None:
                    if game_instance.DimensionManager.get_dimension_boosts() < priority[1]:
                        game_instance.DimensionManager.purchase_upgrade("softReset")
                else:
                    game_instance.DimensionManager.purchase_upgrade("softReset")
            elif priority[0] == "SACRIFICE":
                game_instance.DimensionManager.purchase_sacrifice()
            elif priority[0] == "MAX_TICKSPEED":
                game_instance.DimensionManager.purchase_upgrade("tickSpeedMax")
            elif priority[0] == "BUY_TENS":
                for d_id in range(8, 0, -1):
                    game_instance.DimensionManager.purchase_upgrade(f"M{d_id}")
            elif priority[0] == "BUY_SINGLES":
                for d_id in range(8, 0, -1):
                    game_instance.DimensionManager.purchase_upgrade(f"B{d_id}")