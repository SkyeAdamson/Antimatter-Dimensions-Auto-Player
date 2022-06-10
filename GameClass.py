from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from ChallengeManager import ChallengeManager
from CurrencyManagerClass import CurrencyManager
from DimensionManagerClass import DimensionManager
from BrowserManagerClass import BrowserManager
from InfinityManager import InfinityManager
from StrategyManager import StrategyManager
from selenium.webdriver.common.by import By

class Game:

    def __init__(self, debug_mode = False):
        self.driver = self.create_driver()
        self.debug_mode = debug_mode

    def create_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument(r'--user-data-dir=/home/skye/.config/google-chrome/Default')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.set_page_load_timeout(5)
        return driver     

    def disable_sacrifice_confirmation(self) -> bool:
        """
        Returns true if sacrifice confirmation pop up was successfully disabled; otherwise, returns false.
        """
        sacrifice_checkbox = self.driver.find_element(By.ID, "confirmation")
        if sacrifice_checkbox.is_displayed() and not sacrifice_checkbox.is_selected():
            sacrifice_checkbox.click()
            return True
        else:
            return False

    def create_managers(self):
        self.BrowserManager = BrowserManager(self)
        self.CurrencyManager = CurrencyManager(self)
        self.DimensionManager = DimensionManager(self)
        self.InfinityManager = InfinityManager(self)
        self.StrategyManager = StrategyManager(self)
        self.ChallengeManager = ChallengeManager(self)