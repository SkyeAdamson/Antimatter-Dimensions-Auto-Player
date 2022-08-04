from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

class CurrencyManager:

    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.antimatter = 0

    # Change to get/set
    def get_antimatter_balance(self):
        self.antimatter = float(self.game_instance.BrowserManager.execute_script("return player.money"))

    def get_ip(self):
        return int(float('{:.2e}'.format(float(self.game_instance.BrowserManager.execute_script("return player.infinityPoints")))))

    def get_cost_of_buy_10(self, dimension_id):
        dim_name = ""
        if dimension_id == 1:
            dim_name = "first"
        elif dimension_id == 2:
            dim_name = "second"
        elif dimension_id == 3:
            dim_name = "third"
        elif dimension_id == 4:
            dim_name = "fourth"
        elif dimension_id == 5:
            dim_name = "fifth"
        elif dimension_id == 6:
            dim_name = "sixth"
        elif dimension_id == 7:
            dim_name = "seventh"
        elif dimension_id == 8:
            dim_name = "eight"

        cost = float(self.game_instance.BrowserManager.execute_script(f"return player.{dim_name}Cost")) * 10
        return '{:.2e}'.format(float(cost))
