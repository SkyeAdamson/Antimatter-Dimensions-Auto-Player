from GameClass import Game
from selenium.webdriver.common.by import By
import time

game = Game()
game.create_managers()
if game.BrowserManager.start_browser():
    sacrifice_checkbox = game.driver.find_element(By.ID, "confirmation")
    if sacrifice_checkbox.is_displayed and not sacrifice_checkbox.is_selected():
        sacrifice_checkbox.click()
    while True:
        start_time = time.time()
        game.DimensionManager.purchase_upgrade("secondSoftReset")
        game.DimensionManager.purchase_upgrade("softReset")
        game.DimensionManager.purchase_sacrifice()
        game.DimensionManager.purchase_upgrade("tickSpeed")
        for d_id in range(8, 0):
            game.DimensionManager.purchase_upgrade(f"M{d_id}")
        for d_id in range(8, 0):
            game.DimensionManager.purchase_upgrade(f"B{d_id}")
        end_time = time.time()
        #print(f"Took {end_time - start_time} seconds")
input()