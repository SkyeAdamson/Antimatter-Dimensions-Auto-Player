from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
import itertools

class DimensionManager:

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

    def buy_max_manual(self):
        dim_ids = list(map(lambda x: str(x[0]) + str(x[1]), itertools.product(["B", "M"], range(1, 9)))) + ["tickSpeed", "tickSpeedMax"]
        dim_ids.reverse()
        for id in dim_ids:
            element = self.game_instance.driver.find_element(By.ID, id)
            if element != None:
                if element.is_displayed() and element.get_attribute("class") == "storebtn":
                    element.click()

    def hold_m(self):
        try:
            actions = ActionChains(self.game_instance.driver)
            actions.send_keys('M')
            actions.perform()
        except Exception as ex:
            print("Max buy couldn't run")
            pass

    def purchase_upgrade(self, element_id):
        try:
            if self.game_instance.BrowserManager.load_dimensions():
                self.game_instance.BrowserManager.click_element_if_class(element_id, "storebtn")
        except ElementNotInteractableException as e:
            print(f"Tried to click element associated with {element_id} but was not interactable")
        except ElementClickInterceptedException as e:
            print(f"Tried to click element associated with {element_id} but was not clickable")
        except AttributeError as e:
            print(f"Attribute error for {element_id}")
