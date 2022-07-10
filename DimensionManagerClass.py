from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains

class DimensionManager:

    id_to_string_conversions = {
        1 : "first",
        2 : "second",
        3 : "third",
        4 : "fourth"
    }

    def __init__(self, game_instance):
        self.game_instance = game_instance

    def get_dimension_boosts(self):
        return int(self.game_instance.BrowserManager.execute_script("return player.resets"))

    def get_galaxy_count(self):
        return int(self.game_instance.BrowserManager.execute_script("return player.galaxies"))

    def purchase_sacrifice(self, min_sacrifice_multiplier):
        try:
            sacrifice_button = self.game_instance.driver.find_element(By.ID, "sacrifice")
            if sacrifice_button.is_displayed():
                sacrifice_multiplier = float(((sacrifice_button.text.split(" "))[2])[1:-2])
                if sacrifice_multiplier >= min_sacrifice_multiplier and sacrifice_button.get_attribute("class") != "unavailablebtn":
                    sacrifice_button.click()
        except AttributeError as ex:
            print("Couldn't sacrifice")
        except IndexError as ex:
            print("Couldn't sacrifice")

    def hold_m(self):
        try:
            actions = ActionChains(self.game_instance.driver)
            actions.send_keys('M')
            actions.perform()
        except Exception as ex:
            print("Max buy couldn't run")
            pass

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
        except ElementClickInterceptedException as e:
            print(f"Tried to click element associated with {element_id} but was not clickable")
        except AttributeError as e:
            print(f"Attribute error for {element_id}")
