from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from CurrencyManagerClass import CurrencyManager
from DimensionManagerClass import DimensionManager
from BrowserManagerClass import BrowserManager
from InfinityManager import InfinityManager
from StrategyManager import StrategyManager

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

    def create_managers(self):
        self.BrowserManager = BrowserManager(self)
        self.CurrencyManager = CurrencyManager(self)
        self.DimensionManager = DimensionManager(self)
        self.InfinityManager = InfinityManager(self)
        self.StrategyManager = StrategyManager(self)