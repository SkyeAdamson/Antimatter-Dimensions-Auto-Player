from selenium.webdriver.common.by import By
from math import log2

class InfinityManager:

    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.purchased_upgrades = []
        self.purchased_break_upgrades = []
        self.x2_multi_level = 0
        self.order_to_purchase_infinity_upgrades = [
            (11, 1), 
            (21, 1),
            (22, 1), 
            (23, 1), 
            (24, 2), 
            (12, 1), 
            (13, 1),
            (14, 1),
            (31, 3),
            (32, 5),
            (33, 7),
            (34, 10),
            (41, 20), 
            (42, 40), 
            (43, 80), 
            (44, 500)]

        self.order_to_purchase_break_upgrades = [(11, 1e4), (21, 5e4), (12, 1e5), (22, 1e6)]

    def break_upgrades_still_to_purchase(self):
        return [upgrade[0] for upgrade in self.order_to_purchase_break_upgrades if not upgrade[0] in self.purchased_break_upgrades]

    def are_break_upgrades_available(self):
        """
        Return true if break upgrades are available to purchase
        """

        available_upgrades = self.break_upgrades_still_to_purchase()
        for upgrade in available_upgrades:
            cost = [x[1] for x in self.order_to_purchase_break_upgrades if x[0] == upgrade][0]
            if self.game_instance.CurrencyManager.get_ip() >= cost:
                return True

        if self.x2_available_to_buy():
            return True
        else:
            return False

    def big_crunch(self):
        button_element = self.game_instance.driver.find_element(By.ID, "bigcrunch")
        if button_element.is_displayed():
            button_element.click()
            return True
        else:
            return False

    def enable_break_infinity(self):
        self.game_instance.BrowserManager.click_element_if_inner("break", "BREAK INFINITY",
            self.game_instance.BrowserManager.View.BREAK)

    def get_purchased_infinity_upgrades(self):
        if self.game_instance.BrowserManager.load_infinity_upgrades():
            purchased_upgrades = []
            for column_id in range(1, 5):
                for row_id in range(1, 5):
                    button_element = self.game_instance.driver.find_element(By.ID, f"infi{column_id}{row_id}")
                    if button_element.get_attribute("class") == "infinistorebtnbought":
                        purchased_upgrades.append(int(f"{column_id}{row_id}"))
            return purchased_upgrades
        else:
            return []

    def get_purchased_break_upgrades(self):
        if self.game_instance.BrowserManager.load_break():
            purchased_upgrades = []
            for upgrade in [upgrade[0] for upgrade in self.order_to_purchase_break_upgrades]:
                if self.game_instance.BrowserManager.check_element_class(f"postinfi{upgrade}", "infinistorebtnbought"):
                    purchased_upgrades.append(upgrade)
            return purchased_upgrades
        else:
            return []

    def purchase_max_infinity_upgrades(self):
        if self.game_instance.BrowserManager.load_infinity_upgrades():
            if not len(self.purchased_upgrades) == 16:
                unpurchased = [upgrade for upgrade in self.order_to_purchase_infinity_upgrades if upgrade[0] not in self.purchased_upgrades]
                print(unpurchased)

    def buy_available_upgrades(self):
        if self.game_instance.BrowserManager.load_infinity_upgrades():
            if not len(self.purchased_upgrades) == 16:
                for upgrade_id in self.order_to_purchase_upgrades:
                    if upgrade_id not in self.purchased_upgrades:
                        upgrade_button = self.game_instance.driver.find_element(By.ID, f"infi{upgrade_id}")
                        if upgrade_button.get_attribute("class") == f"infinistorebtn{str(upgrade_id)[1]}":
                            upgrade_button.click()
                        else:
                            break
            else:
                self.purchase_x2_upgrade()
            self.purchased_upgrades = self.get_purchased_infinity_upgrades()
            return True
        else:
            return False

    def get_x2_level(self):
        raw_mult = int(round(float(self.game_instance.BrowserManager.execute_script("return player.infMult"))))
        level = int(round(log2(raw_mult)))
        return level

    def price_of_next_x2(self):
        return 10 ** (self.x2_multi_level + 1)

    def x2_available_to_buy(self):
        if self.game_instance.CurrencyManager.get_ip() >= self.price_of_next_x2():
            return True
        else:
            return False

    def purchase_x2_upgrade(self):
        if self.game_instance.BrowserManager.load_infinity_upgrades():
            x2_button = self.game_instance.driver.find_element(By.ID, f"infiMult")
            while x2_button.get_attribute("class") == "infinimultbtn":
                x2_button.click()
                self.x2_multi_level = self.get_x2_level()

    def buy_available_break_upgrades(self):
        if self.are_break_upgrades_available():
            if self.game_instance.BrowserManager.load_break():
                if not len(self.purchased_break_upgrades) == 16:
                    for upgrade_id in self.order_to_purchase_break_upgrades: # List comp?
                            if upgrade_id[0] not in self.purchased_break_upgrades:
                                element_id = f"postinfi{upgrade_id[0]}"
                                self.game_instance.BrowserManager.click_element_if_class(element_id,
                                    "infinistorebtn1")
                    self.purchased_break_upgrades = self.get_purchased_break_upgrades()
                
                if self.x2_available_to_buy():
                    self.purchase_x2_upgrade()