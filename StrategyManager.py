class StrategyManager:

    def __init__(self, game_instance):
        self.game_instance = game_instance

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