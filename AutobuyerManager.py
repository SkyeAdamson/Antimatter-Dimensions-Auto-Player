from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

class AutobuyerManager:

    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.intervals_maxed = [False] * 12 #0 - 7 for dims, 8 is tickspeed 9 is dimboosts, 10 is galaxies, 11 is big crunch
        self.bulk_maxed = [False] * 8

    def buy_max_upgrades(self):
        '''
        Attempts to purchase any autobuyers that are not yet fully upgraded.
        '''
        btn_suffix_ids = ["1", "2", "3", "4", "5", "6", "7", "8", "TickSpeed", "DimBoost", "Galaxies", "Inf"]
        if self.game_instance.BrowserManager.load_autobuyers():
            for idx in range(0, 8):
                if not(self.intervals_maxed[idx] and self.bulk_maxed[idx]):
                    self.game_instance.BrowserManager.click_element_if_class(
                        f"buyerBtn{btn_suffix_ids[idx]}", "autobuyerbtn"
                    )
                    self.set_interval_maxed(idx)
                    self.set_bulk_maxed(idx)

            for idx in range(8, 12):
                if not self.intervals_maxed[idx]:
                    self.game_instance.BrowserManager.click_element_if_class(
                        f"buyerBtn{btn_suffix_ids[idx]}", "autobuyerbtn"
                    )
                    self.set_interval_maxed(idx)

    def set_autobuyer_priority(self, autobuyer_id, priority):
        element_id = f"priority{autobuyer_id}"
        priority_element = Select(self.game_instance.BrowserManager.return_element_from_id(element_id, 
            self.game_instance.BrowserManager.View.AUTOBUYERS))
        priority_element.select_by_value(f"{priority}")

    def enable_autobuyers(self):
        if self.game_instance.BrowserManager.load_autobuyers():
            for idx in range(1, 13):
                element_id = f"{idx}ison"
                self.game_instance.BrowserManager.click_element_if_not_selected(element_id)
    
    def set_auto_dim_max_8ths(self, value):
        self.game_instance.BrowserManager.send_keys_to_element("priority10", value, clear=True, 
            page_view = self.game_instance.BrowserManager.View.AUTOBUYERS)

    def set_galaxies_to_dim_boost(self, value):
        self.game_instance.BrowserManager.send_keys_to_element("overGalaxies", value, clear=True,
            page_view = self.game_instance.BrowserManager.View.AUTOBUYERS)

    def set_max_galaxies(self, value):
        self.game_instance.BrowserManager.send_keys_to_element("priority11", value, clear=True,
            page_view = self.game_instance.BrowserManager.View.AUTOBUYERS)

    def set_big_crunch_amount(self, value):
        self.game_instance.BrowserManager.send_keys_to_element("priority12", value, clear=True,
            page_view = self.game_instance.BrowserManager.View.AUTOBUYERS)

    def set_interval_maxed(self, autobuyer_id):
        interval = self.game_instance.BrowserManager.execute_script(f"return player.autobuyers[{autobuyer_id}].interval")
        self.intervals_maxed[autobuyer_id] = True if interval == 100 else False

    def set_all_interval_maxed(self):
        for idx in range(0, 12):
            self.set_interval_maxed(idx)

    def set_bulk_maxed(self, autobuyer_id):
        bulk_maxes = [128, 128, 64, 64, 64, 32, 32, 32]
        bulk = self.game_instance.BrowserManager.execute_script(f"return player.autobuyers[{autobuyer_id}].bulk")
        self.bulk_maxed[autobuyer_id] = True if bulk == bulk_maxes[autobuyer_id] else False
    
    def set_all_bulk_maxed(self):
        for idx in range(0, 8):
            self.set_bulk_maxed(idx)