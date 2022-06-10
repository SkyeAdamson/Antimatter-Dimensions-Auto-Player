from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from enum import Enum, auto

class BrowserManager:

    class View(Enum):
        NONE = auto(),
        DIMENSIONS = auto()

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
            return False

    def return_element_by_id(self, id):
        """
        Assumes the correct page view is loaded.
        """
        try:
            element = WebDriverWait(self.game_instance.driver, 5).until(
                EC.visibility_of_element_located((By.ID, id))
            )
            return element
        except TimeoutException:
            return False