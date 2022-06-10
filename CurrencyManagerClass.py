class CurrencyManager:

    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.antimatter = 0

    # Change to get/set
    def get_antimatter_balance(self):
        self.antimatter = float(self.game_instance.driver.execute_script("return player.money"))