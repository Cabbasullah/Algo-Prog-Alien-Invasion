from setting import setting

from ship import ship
from bullet import Bullet
from al1 import Alien
#from mario import Mario
import sys
import pygame
class AlienInvasion:
    def __init__(self):
        #initialize the game and create game resources
        pygame.init()
        self.setting = setting()
         #setting the screen full-screen
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.setting.screen_height=self.screen.get_rect().height
        self.setting.screen_width=self.screen.get_rect().width
        
        pygame.display.set_caption("Alien Invasion")
        self.ship = ship(self)
        #self.mario = Mario(self)
        self.bullet = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()
        
        #set the background color 
        self.bg_color = self.setting.bg_color
    
    def run_game(self):
     while True:
            #calling methods
            self._check_events()
            self.ship.update()
            self._update_bullet()
            self._update_screen()
           
            
           
    def _check_events(self):
        #respond to key presses and mouse events
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    def _check_keydown_events(self, event):
        #respond to key presses
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                elif event.key == pygame.K_q:
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    self._fire_bullet()
    def _check_keyup_events(self, event):  
        #respond to key releases
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False
                    
    def _fire_bullet(self):
        #create a new bullet and add it to the bullet group
        new_bullet = Bullet(self)
        self.bullet.add(new_bullet) 
        if len(self.bullet) < self.setting.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullet.add(new_bullet)
    def _update_bullet(self):
        self.bullet.update()
        for bullet in self.bullet.copy():
            if bullet.rect.bottom <= 0:
                self.bullet.remove(bullet)
                print(len(self.bullet)) 
                
    def _create_fleet(self):
        #create the fleet of aliens
        # Make an alien and find the number of aliens in a row
        # spacing of each alien is equal to one alien width
        alien=Alien(self)
        alien_width = alien.rect.width
        available_space_x = self.setting.screen_width - (1 * alien_width)
        number_aliens_x = available_space_x // (1 * alien_width)
        
        #determine the number of rows of aliens that fit on the screen
        #ship_height = self.ship.rect.height
        #available_space_y = (self.setting.screen_height - (3 * alien_height) - ship_height)
        #number_rows = available_space_y // (2 * alien_height)
        
        #create the first row of aliens

        for alien_number in range(number_aliens_x):
            alien =Alien(self)
            alien.x = alien_width + 1 * alien_width * alien_number
            alien.rect.x = alien.x 
            self.aliens.add(alien)
    
            
                
    #def _create_alien(self, alien_number, row_number):
        #create an alien and place it in the row
       # aliens = aliens(self)
        #alien_width, alien_height = aliens.rect.size
        ##aliens.x = alien_width + 2 (* alien_width) *(alien_number)
        #aliens.rect.x = aliens.x
        #aliens.rect.y = alien_height + 2 * aliens.rect.height * row_number
        #self.aliens.add(aliens)   
        # create the first row of aliens
    
            #create an alien and place it in the row
    def _update_screen(self):
        ##Update images on the screen, and flip to the new screen
        self.screen.fill(self.setting.bg_color)
        self.ship.blitme()
       
        #self.mario.blitme()
        for bullet in self.bullet.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
         
            #Make the most recently drawn screen visible
        pygame.display.flip()
if __name__ == '__main__':
    #make game instance, and run the game 
    ai = AlienInvasion()
    ai.run_game()
            
    
    
