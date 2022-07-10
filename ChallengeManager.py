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
                element_id = f"challenge{self.challenge_conversion_table[challenge_id]}"
                if self.game_instance.BrowserManager.check_element_class(element_id, "completedchallengesbtn"):
                    completed_challenges.append(challenge_id)
            return completed_challenges
        else:
            return []

    def get_active_challenge(self):
        if self.game_instance.BrowserManager.load_challenges():
            for challenge_id in self.challenge_conversion_table.keys():
                element_id = f"challenge{self.challenge_conversion_table[challenge_id]}"
                if self.game_instance.BrowserManager.check_element_class(element_id, "onchallengebtn"):
                    return challenge_id
            return None
        return None

    def start_challenge(self, challenge_id):
        element_id = f"challenge{self.challenge_conversion_table[challenge_id]}"
        self.game_instance.BrowserManager.click_element_if_not_class(element_id, "onchallengesbtn", 
            self.game_instance.BrowserManager.View.CHALLENGES)