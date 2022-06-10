from GameClass import Game
from selenium.webdriver.common.by import By
import time

game = Game(debug_mode=False)
game.create_managers()
if game.BrowserManager.start_browser():
    sacrifice_checkbox = game.driver.find_element(By.ID, "confirmation")
    if sacrifice_checkbox.is_displayed and not sacrifice_checkbox.is_selected():
        sacrifice_checkbox.click()
    game.InfinityManager.purchased_upgrades = game.InfinityManager.get_purchased_infinity_upgrades()
    print(game.BrowserManager.load_dimensions())
    while game.debug_mode == False:
        start_time = time.time()
        game.InfinityManager.big_crunch()
        if game.DimensionManager.get_galaxy_count() < 2:
            game.DimensionManager.purchase_upgrade("secondSoftReset")
        if game.DimensionManager.get_dimension_boosts() < 16:
            game.DimensionManager.purchase_upgrade("softReset")
        game.DimensionManager.purchase_sacrifice()
        game.DimensionManager.purchase_upgrade("tickSpeed")
        for d_id in range(8, 0, -1):
            game.DimensionManager.purchase_upgrade(f"M{d_id}")
        for d_id in range(8, 0, -1):
            game.DimensionManager.purchase_upgrade(f"B{d_id}")
        end_time = time.time()
        #print(f"Took {end_time - start_time} seconds")
input()