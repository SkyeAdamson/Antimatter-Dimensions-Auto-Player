from GameClass import Game

game = Game(debug_mode=False)
game.create_managers()
if game.BrowserManager.start_browser():

    #TODO:
    # - Need a way to get back to Upgrades from sub-tabs
    # - Need to split x2 multiplier upgrade into own function
    # - Need to initalise auto retry challenge to false. 
    # - Support lists for active_challenge modifier to pre-define one strat for multiple challenges
    # - Find element checks in browser manager (PARTIALLY DONE)
    # - Set auto big crunch amount

    game.disable_sacrifice_confirmation()
    game.manager_pre_checks() # Set up managers with any required data
    game.StrategyManager.current_strategy = game.StrategyManager.choose_current_strategy()
    game.StrategyManager.perform_strategy_setup()
    game.BrowserManager.load_dimensions()
    while game.debug_mode == False:
        game.StrategyManager.current_strategy.execute_strategy(game)
input()