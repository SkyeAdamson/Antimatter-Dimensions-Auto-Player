from mysqlx import View
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from enum import Enum, auto

class BrowserManager:

    class View(Enum):
        NONE = auto(),
        DIMENSIONS = "dimensions"
        INFINITY = "infinity"
        CHALLENGES = "challenges"
        AUTOBUYERS = "autobuyers"
        BREAK = "break"

    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.current_view = self.View.NONE

    def start_browser(self):
        self.game_instance.driver.get("https://aarextiaokhiao.github.io/IvarK.github.io/")
        WebDriverWait(self.game_instance.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "coinAmount"))
        )
        # Add in checking method
        self.current_view = self.View.DIMENSIONS
        return True

    def load_dimensions(self):
        if self.current_view == self.View.DIMENSIONS:
            return True
        else:
            dimensions_button = self.game_instance.driver.find_element(By.ID, "dimensionsbtn")
            if dimensions_button.is_displayed():
                dimensions_button.click()
                self.current_view = self.View.DIMENSIONS
                return True
            else:
                return False

    def load_infinity(self):
        if self.current_view == self.View.INFINITY:
            return True
        else:
            try:
                infinity_button = WebDriverWait(self.game_instance.driver, 3).until(
                    EC.element_to_be_clickable((By.ID, "infinitybtn"))
                )
            except TimeoutException as ex:
                print("Infinity Button not clickable in time frame")
                return False

            if infinity_button.is_displayed():
                infinity_button.click()
                self.current_view = self.View.INFINITY
                return True
            else:
                return False

    def load_autobuyers(self):
        if self.current_view == self.View.AUTOBUYERS:
            return True
        else:
            if self.load_infinity():
                try:
                    autobuyer_button = WebDriverWait(self.game_instance.driver, 3).until(
                        EC.element_to_be_clickable((By.ID, "autobuyersbtn"))
                    )
                except TimeoutException as ex:
                    print("Autobuyer Button not clickable in time frame")
                    return False

                if autobuyer_button.is_displayed():
                    autobuyer_button.click()
                    self.current_view = self.View.AUTOBUYERS
                    return True
                else:
                    return False
            else:
                return False

    def load_break(self):
        if self.current_view == self.View.BREAK:
            return True
        else:
            if self.load_infinity():
                try:
                    break_button = WebDriverWait(self.game_instance.driver, 3).until(
                        EC.element_to_be_clickable((By.ID, "postinfbtn"))
                    )
                except TimeoutException as ex:
                    print("Break Infinity Menu Button not clickable in time frame")
                    return False

                if break_button.is_displayed():
                    break_button.click()
                    self.current_view = self.View.BREAK
                    return True
                else:
                    return False
            else:
                return False       

    def load_challenges(self):
        if self.current_view == self.View.CHALLENGES:
            return True
        else:
            try:
                challenges_button = WebDriverWait(self.game_instance.driver, 2).until(
                    EC.element_to_be_clickable((By.ID, "challengesbtn"))
                )
            except TimeoutException as ex:
                print("Infinity Button not clickable in time frame")
                return False
            
            if challenges_button.is_displayed():
                challenges_button.click()
                self.current_view = self.View.CHALLENGES
                return True
            else:
                return False

    def return_element_from_id(self, id : str, page_view : View = None) -> WebElement:
        if page_view != None:
            load_method = getattr(self, f"load_{page_view.value}")

        if page_view == None or load_method():
            try:
                element = WebDriverWait(self.game_instance.driver, 5).until(
                    EC.visibility_of_element_located((By.ID, id))
                )
                return element
            except TimeoutException:
                print(f"Element with id {id} not visible on page")
                return None

    def check_element_class(self, id : str, element_class : str, page_view : View = None) -> bool:
        element = self.return_element_from_id(id, page_view)
        if element != None:
            return element.get_attribute("class") == element_class

    def click_element_if_class(self, id : str, element_class : str, page_view : View = None):
        element = self.return_element_from_id(id, page_view)
        if element != None and element.get_attribute("class") == element_class:
            element.click()

    def click_element_if_not_class(self, id : str, element_class : str, page_view : View = None):
        element = self.return_element_from_id(id, page_view)
        if element != None and element.get_attribute("class") != element_class:
            element.click()
            
    def click_element_if_not_selected(self, id : str, page_view : View = None):
        element = self.return_element_from_id(id, page_view)
        if element != None and not element.is_selected():
            element.click()

    def click_element_if_inner(self, id : str, inner_html : str, page_view : View = None):
        element = self.return_element_from_id(id, page_view)
        if element != None and element.get_attribute("innerHTML") == inner_html:
            element.click()

    def send_keys_to_element(self, id : str, keys : str, clear : bool = False, page_view : View = None):
        element = self.return_element_from_id(id, page_view)
        if element != None:
            if clear : element.clear()
            element.send_keys(keys)

    def execute_script(self, script : str):
        return self.game_instance.driver.execute_script(script)