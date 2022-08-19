import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class Strategy:

    def __init__(self, name, priority_list, conditions, modifiers):
        self.name = name
        self.priority_list = priority_list
        self.conditions = conditions

        for key in modifiers.keys():
            setattr(self, key, modifiers[key])

    def conditions_met(self, game_instance):
        all_conditions_met = True
        for condition in self.conditions:
            if condition[0] == "IP_MULT_LEVEL":
                if game_instance.InfinityManager.x2_multi_level < condition[1]:
                    all_conditions_met = False
            elif condition[0] == "MAX_IP":
                infinites = int(game_instance.driver.execute_script("return player.infinitied"))
                if infinites > condition[1]:
                    all_conditions_met = False
            elif condition[0] == "MIN_IP":
                infinites = int(game_instance.driver.execute_script("return player.infinitied"))
                if infinites < condition[1]:
                    all_conditions_met = False
            elif condition[0] == "INF_UPGRADE_PURCHASED":
                if condition[1] not in game_instance.InfinityManager.purchased_upgrades:
                    all_conditions_met = False
            elif condition[0] == "CHALLENGE_COMPLETED":
                if condition[1] not in game_instance.ChallengeManager.completed_challenges:
                    all_conditions_met = False
            elif condition[0] == "AUTOBUYER_INTERVALS_MAXED":
                interval_set = set(game_instance.AutobuyerManager.intervals_maxed)
                if not (len(interval_set) == 1 and list(interval_set)[0] == True):
                    all_conditions_met = False
        return all_conditions_met


    def execute_strategy(self, game_instance):
        for priority in self.priority_list:
            if priority[0] == "BUY_BREAK_UPS":
                game_instance.InfinityManager.buy_available_break_upgrades()
                game_instance.BrowserManager.load_dimensions()
                game_instance.StrategyManager.current_strategy = game_instance.StrategyManager.choose_current_strategy()
                if game_instance.StrategyManager.current_strategy != game_instance.StrategyManager.last_strategy:
                    game_instance.StrategyManager.perform_strategy_setup()
            elif priority[0] == "BIG_CRUNCH":
                if game_instance.InfinityManager.big_crunch():
                    try:
                        dim_button = WebDriverWait(game_instance.driver, 3).until(
                            EC.element_to_be_clickable((By.ID, "dimensionsbtn"))
                        )
                        WebDriverWait(game_instance.driver, 3).until(
                            EC.invisibility_of_element((By.ID, "bigcrunch"))
                        )
                    except TimeoutException as ex:
                        print("Dimension Button not clickable in time frame")

                    if not self.on_big_crunch == None:
                        for priority in self.on_big_crunch:
                            if priority == "autobuyers":
                                game_instance.AutobuyerManager.buy_max_upgrades()
                            elif priority == "infinity_upgrades":
                                game_instance.InfinityManager.buy_available_upgrades()

                    game_instance.ChallengeManager.completed_challenges = game_instance.ChallengeManager.get_completed_challenges()
                    game_instance.BrowserManager.load_dimensions()
                    game_instance.StrategyManager.current_strategy = game_instance.StrategyManager.choose_current_strategy()
                    game_instance.StrategyManager.perform_strategy_setup()
                    break
            elif priority[0] == "ANTIMATTER_GALAXY":
                if priority[1] != None:
                    if game_instance.DimensionManager.get_galaxy_count() < priority[1]:
                        game_instance.DimensionManager.purchase_upgrade("secondSoftReset")
                else:
                    game_instance.DimensionManager.purchase_upgrade("secondSoftReset")
            elif priority[0] == "DIMENSION_BOOST":
                if priority[1] != None:
                    if game_instance.DimensionManager.get_dimension_boosts() < priority[1]:
                        game_instance.DimensionManager.purchase_upgrade("softReset")
                else:
                    game_instance.DimensionManager.purchase_upgrade("softReset")
            elif priority[0] == "SACRIFICE":
                if priority[1] != None:
                    game_instance.DimensionManager.purchase_sacrifice(priority[1])
                else:
                    game_instance.DimensionManager.purchase_sacrifice(2)
            elif priority[0] == "MAX_ALL":
                game_instance.DimensionManager.hold_m()
            elif priority[0] == "MAX_MANUAL":
                game_instance.DimensionManager.buy_max_manual()
            elif priority[0] == "MAX_TICKSPEED":
                game_instance.DimensionManager.purchase_upgrade("tickSpeedMax")
            elif priority[0] == "BUY_TENS":
                for d_id in range(8, 0, -1):
                    game_instance.DimensionManager.purchase_upgrade(f"M{d_id}")
            elif priority[0] == "BUY_SINGLES":
                for d_id in range(8, 0, -1):
                    game_instance.DimensionManager.purchase_upgrade(f"B{d_id}")
            elif priority[0] == "C9_STRATEGY": # Need a better method
                current_dim_boosts = game_instance.DimensionManager.get_dimension_boosts()
                current_galaxies = game_instance.DimensionManager.get_galaxy_count()
                while current_dim_boosts < 5:
                    for d_id in range(1, 5 + (current_dim_boosts)):
                        game_instance.DimensionManager.purchase_upgrade(f"M{d_id}")
                    game_instance.DimensionManager.purchase_upgrade("softReset")
                    while not game_instance.DimensionManager.get_dimension_boosts() == current_dim_boosts + 1:
                        for d_id in range(4 + current_dim_boosts, 0, -1):
                            game_instance.DimensionManager.purchase_upgrade(f"M{d_id}")
                        game_instance.DimensionManager.purchase_upgrade("softReset")
                    current_dim_boosts = game_instance.DimensionManager.get_dimension_boosts()

                while current_dim_boosts >= 5:
                    for d_id in range(8, 0, -1):
                        if d_id < 8 and game_instance.CurrencyManager.get_cost_of_buy_10(d_id) != game_instance.CurrencyManager.get_cost_of_buy_10(8):
                            game_instance.DimensionManager.purchase_upgrade(f"M{d_id}")
                        elif d_id == 8:
                            game_instance.DimensionManager.purchase_upgrade(f"M8")
                    game_instance.DimensionManager.purchase_upgrade("tickSpeed")
                    for d_id in range(8, 0, -1):
                        if d_id < 8 and game_instance.CurrencyManager.get_cost_of_buy_10(d_id) != game_instance.CurrencyManager.get_cost_of_buy_10(8):
                            game_instance.DimensionManager.purchase_upgrade(f"M{d_id}")
                        elif d_id == 8:
                            game_instance.DimensionManager.purchase_upgrade(f"M8")
                    if game_instance.InfinityManager.big_crunch():
                        time.sleep(2)
                        game_instance.InfinityManager.buy_available_upgrades()
                        game_instance.ChallengeManager.completed_challenges = game_instance.ChallengeManager.get_completed_challenges()
                        game_instance.BrowserManager.load_dimensions()
                        game_instance.StrategyManager.current_strategy = game_instance.StrategyManager.choose_current_strategy()
                        game_instance.StrategyManager.perform_strategy_setup()
                        break
                    game_instance.DimensionManager.purchase_upgrade("secondSoftReset")
                    if game_instance.DimensionManager.get_galaxy_count() == current_galaxies + 1:
                        current_galaxies = game_instance.DimensionManager.get_galaxy_count()
                        current_dim_boosts = game_instance.DimensionManager.get_dimension_boosts()
                        break
                    game_instance.DimensionManager.purchase_upgrade("softReset")
                    if game_instance.DimensionManager.get_dimension_boosts() == current_dim_boosts + 1:
                        current_dim_boosts = game_instance.DimensionManager.get_dimension_boosts()

                    