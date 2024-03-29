from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from AutobuyerManager import AutobuyerManager
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

    def disable_challenge_auto_retry(self) -> bool:
        """
        Returns true if auto retry was successfully disabled
        """
        auto_retry = self.BrowserManager.return_element_from_id("retry", self.BrowserManager.View.OTHER_OPTIONS)
        if auto_retry.get_attribute("innerHTML") == "Automatically retry challenges: ON":
            auto_retry.click()
            return True
        else:
            return False

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
        self.AutobuyerManager = AutobuyerManager(self)

    def manager_pre_checks(self):
        if self.BrowserManager.load_infinity():
            self.InfinityManager.x2_multi_level = self.InfinityManager.get_x2_level()
            self.InfinityManager.purchased_upgrades = self.InfinityManager.get_purchased_infinity_upgrades()
            self.InfinityManager.buy_available_upgrades()
            if len(self.InfinityManager.purchased_upgrades) == 16:
                self.InfinityManager.purchased_break_upgrades = self.InfinityManager.get_purchased_break_upgrades()
        if self.BrowserManager.load_challenges():
            self.ChallengeManager.completed_challenges = self.ChallengeManager.get_completed_challenges()
            self.ChallengeManager.active_challenge = self.ChallengeManager.get_active_challenge()
        if self.BrowserManager.load_autobuyers():
            self.AutobuyerManager.set_all_interval_maxed()
            self.AutobuyerManager.set_all_bulk_maxed()
        
        self.StrategyManager.construct_strategies_from_json()