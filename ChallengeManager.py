from selenium.webdriver.common.by import By

class ChallengeManager:

    # Converts the challenge's written ID to the element ID
    challenge_conversion_table = {
        1: 1,
        2: 2,
        3: 3,
        4: 8,
        5: 6,
        6: 10,
        7: 9,
        8: 11,
        9: 5,
        10: 4,
        11: 12,
        12: 7
    }

    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.completed_challenges = []
        self.active_challenge = None

    def get_completed_challenges(self):
        if self.game_instance.BrowserManager.load_challenges():
            completed_challenges = []
            for challenge_id in self.challenge_conversion_table.keys():
                button_element = self.game_instance.driver.find_element(By.ID, f"challenge{self.challenge_conversion_table[challenge_id]}")
                if button_element.get_attribute("class") == "completedchallengesbtn":
                    completed_challenges.append(challenge_id)
            return completed_challenges
        else:
            return []

    def get_active_challenge(self):
        if self.game_instance.BrowserManager.load_challenges():
            for challenge_id in self.challenge_conversion_table.keys():
                challenge_button = self.game_instance.driver.find_element(By.ID, f"challenge{self.challenge_conversion_table[challenge_id]}")
                if challenge_button.get_attribute("class") == "onchallengebtn":
                    return challenge_id
            return None
        return None

    def start_challenge(self, challenge_id):
        if self.game_instance.BrowserManager.load_challenges():
            challenge_button = self.game_instance.driver.find_element(By.ID, f"challenge{self.challenge_conversion_table[challenge_id]}")
            if challenge_button.get_attribute("class") != "onchallengebtn":
                challenge_button.click()
                return True
            else:
                return True
        else:
            return False