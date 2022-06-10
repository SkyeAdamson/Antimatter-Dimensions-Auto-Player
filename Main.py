from GameClass import Game
from selenium.webdriver.common.by import By
import time

game = Game(debug_mode=True)
game.create_managers()
if game.BrowserManager.start_browser():
    sacrifice_checkbox = game.driver.find_element(By.ID, "confirmation")
    if sacrifice_checkbox.is_displayed and not sacrifice_checkbox.is_selected():
        sacrifice_checkbox.click()
    game.InfinityManager.purchased_upgrades = game.InfinityManager.get_purchased_infinity_upgrades()
    print(game.BrowserManager.load_dimensions())
    while game.debug_mode == False:
        start_time = time.time()
        if game.InfinityManager.big_crunch():
            game.InfinityManager.buy_available_upgrades()
        game.StrategyManager.pre_infinity_strategy()
        end_time = time.time()
        #print(f"Took {end_time - start_time} seconds")
input()