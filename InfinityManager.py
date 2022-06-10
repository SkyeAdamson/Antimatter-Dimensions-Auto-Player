from selenium.webdriver.common.by import By

class InfinityManager:

    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.purchased_upgrades = []
        self.order_to_purchase_upgrades = [11, 21, 22, 23, 24, 12, 13, 14, 31, 32, 33, 34, 41, 42, 43, 44]

    def big_crunch(self):
        button_element = self.game_instance.driver.find_element(By.ID, "bigcrunch")
        if button_element.is_displayed():
            button_element.click()
            return True
        else:
            return False

    def get_purchased_infinity_upgrades(self):
        if self.game_instance.BrowserManager.load_infinity():
            purchased_upgrades = []
            for column_id in range(1, 5):
                for row_id in range(1, 5):
                    button_element = self.game_instance.driver.find_element(By.ID, f"infi{column_id}{row_id}")
                    if button_element.get_attribute("class") == "infinistorebtnbought":
                        purchased_upgrades.append(int(f"{column_id}{row_id}"))
            return purchased_upgrades
        else:
            return []

    def buy_available_upgrades(self):
        if self.game_instance.BrowserManager.load_infinity():
            for upgrade_id in self.order_to_purchase_upgrades:
                if upgrade_id not in self.purchased_upgrades:
                    upgrade_button = self.game_instance.driver.find_element(By.ID, f"infi{upgrade_id}")
                    if upgrade_button.get_attribute("class") == "infinistorebtn1":
                        upgrade_button.click()
            self.purchased_upgrades = self.get_purchased_infinity_upgrades()
            return True
        else:
            return False

