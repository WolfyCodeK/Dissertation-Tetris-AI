import pygame
from controllers.game_controller import GameController
from controllers.window import Window
from utils.screen_sizes import ScreenSizes
import utils.game_analysis as gu

if __name__ == '__main__':    
    game = GameController()
    
    # Pygame intial setup
    pygame.display.init()
    pygame.font.init()
    
    window = Window(game, ScreenSizes.MEDIUM)
    
    pygame.display.set_caption("Tetris - Pygame")
    
    running = True

    while running:
        # Check if user has quit the window
        if (pygame.event.get(pygame.QUIT)):
            running = False
            
        game._cycle_game_clock()    
        event_list = pygame.event.get()
        game.take_player_inputs(event_list)
        
        done = game._run_logic()

        for event in event_list:     
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    done = True
                    
        window.draw()
        
        if done:
            game.reset_game()
            reward = 0       