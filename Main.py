from GameClass import Game

game = Game(debug_mode=False)
game.create_managers()
if game.BrowserManager.start_browser():

    #TODO:
    # - Support lists for active_challenge modifier to pre-define one strat for multiple challenges
    # - Find element checks in browser manager (PARTIALLY DONE)
    # - Add strat for max all after 1st dim shiftf
    # - Challenge resetting during early inf stage
    # - Set autobuyers to buy 10/max
    # - Weird bug with infinity upgrades going to production screen, can't find Infinity div element
    # - Multi post-break upgrades purchasing
    # - Smarter way to deal with upgrading, only doing it when upgrade can be bought?

    game.disable_sacrifice_confirmation()
    game.disable_challenge_auto_retry()
    game.manager_pre_checks() # Set up managers with any required data
    game.StrategyManager.current_strategy = game.StrategyManager.choose_current_strategy()
    game.StrategyManager.perform_strategy_setup()
    game.BrowserManager.load_dimensions()
    while game.debug_mode == False:
        game.StrategyManager.current_strategy.execute_strategy(game)
input()