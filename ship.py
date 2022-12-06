import pygame
from pygame.sprite import Sprite
class ship(Sprite):
    
    def __init__(self, ai_game):
        #initialize the ship and set its statring position
        super().__init__()
        self.screen = ai_game.screen
        self.setting =ai_game.setting
        self.screen_rect =ai_game.screen.get_rect()
        
        
        #load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        #start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        
        #store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)
        
        #movement flag
        self.moving_right = False
        self.moving_left = False
        #self.moving_up = False
        #self.moving_down = False
    def update(self): 
        #update the ship's position based on the movement flag
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.setting.ship_speed
        if self.moving_left and self.rect.left > 0:
           self.x -= self.setting.ship_speed
        #if self.moving_up:
           # self.rect.y += 1
        #if self.moving_down:
            #self.rect.y -= 1
        #update rect object from self.x 
        self.rect.x = self.x
    
    def blitme(self):
        #draw the ship at its current location
        self.screen.blit(self.image, self.rect)
        
    def center_ship(self):
        #center the ship on the screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = (self.rect.x)
        
    