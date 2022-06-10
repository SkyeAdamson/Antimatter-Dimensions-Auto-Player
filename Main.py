from GameClass import Game

game = Game(debug_mode=True)
game.create_managers()
if game.BrowserManager.start_browser():
    game.disable_sacrifice_confirmation()
    game.InfinityManager.purchased_upgrades = game.InfinityManager.get_purchased_infinity_upgrades()
    game.ChallengeManager.completed_challenges = game.ChallengeManager.get_completed_challenges()
    game.ChallengeManager.active_challenge = game.ChallengeManager.get_active_challenge()
    print(game.ChallengeManager.active_challenge)
    game.BrowserManager.load_dimensions()
    while game.debug_mode == False:
        if game.InfinityManager.big_crunch():
            game.InfinityManager.buy_available_upgrades()
        game.StrategyManager.pre_infinity_strategy()
input()