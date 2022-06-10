from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException

class DimensionManager:

    id_to_string_conversions = {
        1 : "first",
        2 : "second",
        3 : "third",
        4 : "fourth"
    }

    def __init__(self, game_instance):
        self.game_instance = game_instance

    def purchase_sacrifice(self):
        sacrifice_button = self.game_instance.driver.find_element(By.ID, "sacrifice")
        if sacrifice_button.is_displayed():
            sacrifice_multiplier = float(((sacrifice_button.text.split(" "))[2])[1:-2])
            if sacrifice_multiplier >= 2:
                sacrifice_button.click()

    def upgrade_purchasable(self, element):
        if element.get_attribute("class") == "storebtn":
            return True
        else:
            return False

    def purchase_upgrade(self, element_id):
        try:
            if self.game_instance.BrowserManager.load_dimensions():
                button_element = self.game_instance.driver.find_element(By.ID, element_id)
                if self.upgrade_purchasable(button_element) and button_element.is_displayed():
                    button_element.click()
        except ElementNotInteractableException as e:
            print(f"Tried to click element associated with {element_id} but was not interactable")