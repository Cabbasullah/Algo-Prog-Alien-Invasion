class setting():
#A class to store all settings for Alien Invasion.
    def __init__(self):
        #initializing the game's static settings
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255,255,255)
        #speed adjustment
        self.ship_speed = 1.5
        self.ship_limit=3
        
        #bullet setting
        self.bullet_speed = 3.0
        self.bullet_width = 8
        self.bullet_height = 11
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 4
        
        #alien setting
        #self.alien_speed = 5
        self.fleet_drop_speed = 6
        
        #How quickly the game speeds up
        self.speedup_scale = 1.1
        #How quickly the alien point values increase
        self.score_scale = 1.5
         
        self.initialize_dynamic_setting()
    def initialize_dynamic_setting(self):
        #initialize setting that changes throughout the game
        self.ship_limit=1.5
        self.bullet_speed= 3.0
        self.alien_speed=1.0
        
         # fleet_direction of 1 reprsents right; -1 represents left
        self.fleet_direction = 1
        
        #scoring
        self.alien_points= 5
    def increase_speed(self):
        #Increase speed setting
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
    
        self.alien_points = int(self.alien_points * self.score_scale)
       
        
        
    