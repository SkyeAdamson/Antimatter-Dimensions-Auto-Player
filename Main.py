from GameClass import Game

game = Game(debug_mode=False)
game.create_managers()
if game.BrowserManager.start_browser():

    # Manager and game set up
    game.disable_sacrifice_confirmation()
    game.InfinityManager.purchased_upgrades = game.InfinityManager.get_purchased_infinity_upgrades()
    game.ChallengeManager.completed_challenges = game.ChallengeManager.get_completed_challenges()
    game.ChallengeManager.active_challenge = game.ChallengeManager.get_active_challenge()
    game.StrategyManager.construct_strategies_from_json()
    game.StrategyManager.current_strategy = game.StrategyManager.choose_current_strategy()

    game.BrowserManager.load_dimensions()
    while game.debug_mode == False:
        game.StrategyManager.current_strategy.execute_strategy(game)
input()