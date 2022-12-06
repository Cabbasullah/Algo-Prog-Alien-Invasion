class gamestats:
    #Track statistics for Alien Invasion
    
    def __init__(self, ai_game):
        #initialize statistics 
        self.setting = ai_game.setting
        self.reset_stats()
        # start Alien Invasion in an inactive state
        self.game_active =  False
        
        #High score should never be reset
        self.high_score = 0 
    def reset_stats(self):
        ##initialize statistics that can change during the game
        self.ships_left = self.setting.ship_limit
        self.score = 0
        self.level = 1
    
        