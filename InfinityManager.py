from selenium.webdriver.common.by import By

class InfinityManager:

    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.purchased_upgrades = []

    def big_crunch(self):
        button_element = self.game_instance.driver.find_element(By.ID, "bigcrunch")
        if button_element.is_displayed():
            button_element.click()

    def get_purchased_infinity_upgrades(self):
        if self.game_instance.BrowserManager.load_infinity():
            purchased_upgrades = []
            for column_id in range(1, 5):
                for row_id in range(1, 5):
                    button_element = self.game_instance.driver.find_element(By.ID, f"infi{column_id}{row_id}")
                    if button_element.get_attribute("class") == "infinistorebtnbought":
                        purchased_upgrades.append(int(f"{column_id}{row_id}"))
            return purchased_upgrades
