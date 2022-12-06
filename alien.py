from setting import setting
from time import sleep
from scoreboard import scoreboard 
from gamestat import gamestats
from button import button
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
        #create an istance to store game statistics
        self.stats = gamestats(self)
        self.sb = scoreboard(self)
        self.ship = ship(self)
        #self.mario = Mario(self)
        self.bullet = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        
        self._create_fleet()
        #defining/calling play button method
        self.play_button = button(self, "Play")
        
        #set the background color 
        self.bg_color = self.setting.bg_color
    
    def run_game(self):
     while True:
        self._check_events()
         
        if self.stats.game_active:
            #calling methods
            self.ship.update()
            self._update_bullet()
            self._update_aliens()
            
            
         
            
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    def _check_play_button(self, mouse_pos):
        #start a new game when the player click play
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        #reset the game setting
        self.setting.initialize_dynamic_setting()
        if button_clicked and not self.stats.game_active:
            #reset the game statistice
            self.stats.reset_stats()
            self.stats.game_active=True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            #get rid of any remaining aliens and bullets  
            self.aliens.empty()
            self.bullet.empty()
            
            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            
            #hide the mouse cursor
        pygame.mouse.set_visible(False)
                
                
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
        #get rid of bullets that have disappeared
        for bullet in self.bullet.copy():
            if bullet.rect.bottom <= 0:
                self.bullet.remove(bullet)
        self._check_bullet_alien_collisions()
    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullet, self.aliens, True, True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.setting.alien_points*len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            
        #check any bullets that hit aliens
        #if so, get rid of the bullet and aliens
       
        
        if not self.aliens:
            #destroy existing bullets and create new  fleet
            self.bullet.empty()
            self._create_fleet()
            self.setting.increase_speed()
            
            #increase level
            self.stats.level += 1
            self.sb.prep_level()
    
    def _update_aliens(self):
        #check the fleet is at an edge, then update the positions of all aliens in the fleet..
        self._check_fleet_edges()
        self.aliens.update()
        
        #look for alien ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            #print("Ship hit!!!")
            
            #look for the aliens hitting the bottom of the screen
        self._check_alien_bottom()
        
    def _ship_hit(self):
        #respond ot the ship being hit by an alien
        if self.stats.ships_left>0:
             #decrment ships_left
            self.stats.ships_left -=1
            self.sb.prep_ships()
        
            #get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullet.empty()
        
             #create a new fleet and center the ship
        
            self._create_fleet()
            self.ship.center_ship()
            #pause
            sleep (0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
        
    def _check_alien_bottom(self):
        #check if any aliens have reached the bottom of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Treat this the same as if the ship got hit
                self._ship_hit()
                break
        
            
        
                  
    def _create_fleet(self):
        alien=Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.setting.screen_width - (1 * alien_width)
        number_aliens_x = available_space_x // (1 * alien_width)
        
        #determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.setting.screen_height - (1 * alien_height) - ship_height)
        number_rows = available_space_y // (1 * alien_height)
        
        #create full fleet
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
            #alien =Alien(self)
            #alien.x = alien_width + 1 * alien_width * alien_number
            #alien.rect.x = alien.x 
            #self.aliens.add(alien)
    
            
                
    def _create_alien(self, alien_number, row_number):
        #create an alien and place it in the row
        aliens = Alien(self) 
        alien_width, alien_height = aliens.rect.size
        aliens.x = alien_width + 1 * alien_width *alien_number
        aliens.rect.x = aliens.x
        aliens.rect.y = alien_height + 1 * aliens.rect.height * row_number
        self.aliens.add(aliens)   
        
        
    def _check_fleet_edges(self):
        #respond appropriately if any aliens have reached and edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
                
                
    def _change_fleet_direction(self):
        #drop the entire fleet and change the fleet's direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.setting.fleet_drop_speed
            self.setting.fleet_direction *=-1
            break
            
        #drop the entire fleet and change the fleet's direction
        
        # create the first row of aliens
    
            #create an alien and place it in the row
    def _update_screen(self):
        ##Update images on the screen, and flip to the new screen
        self.screen.fill(self.setting.bg_color)
        self.ship.blitme()
        for bullet in self.bullet.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        
         #draw score information on the screen
        self.sb.show_score()
         
        #draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
       
        
        
         
            #Make the most recently drawn screen visible
        pygame.display.flip()
if __name__ == '__main__':
    #make game instance, and run the game 
    ai = AlienInvasion()
    ai.run_game()
            
    
    