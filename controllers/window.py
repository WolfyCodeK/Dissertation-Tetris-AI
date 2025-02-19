import pygame
import os

from game.game_settings import GameSettings
import utils.board_constants as bc
import utils.window_utils as win_utils
from controllers.game_controller import GameController

class Window():
    def __init__(self, game: GameController, screen_size: int, show_fps: bool = True, show_score: bool = True, show_queue = True) -> None:
        # Set window position
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(500, 150)
        
        # Configure window settings
        GameSettings.show_fps = show_fps
        GameSettings.show_score = show_score
        GameSettings.show_queue = show_queue
        GameSettings.set_screen_size(screen_size)
        
        # Set Icon and title
        pygame.display.set_caption("Tetris Environment")
        tetris_icon = pygame.image.load("res/tetris_icon.png")
        pygame.display.set_icon(tetris_icon)
        
        # Set game controller
        self.game = game
        self.render_game = True
        
        # Colour values
        self.FPS_COLOUR = (0, 255, 0)
        self.SCORE_COLOUR = (255, 255, 255)
        self.B2B_COLOUR = (255, 0, 0)
        self.BG_FILL = 0
        
        # Set fps string
        self.font = pygame.font.Font("freesansbold.ttf", win_utils.get_grid_size())
        self.fps_string = self.font.render(str("- - -"), True, self.FPS_COLOUR)
        
        # Set score string
        self.score_string = self.font.render(str(self.game.score), True, (255, 255, 255))
        
        # Set back to back string
        self.b2b_string = self.font.render(str(self.game.b2b), True, (255, 255, 255))
        
        # Set window and surface sizes
        self.scr_width, self.scr_height = win_utils.get_screen_sizes()
        self.window = pygame.display.set_mode((self.scr_width, self.scr_height))
        self.board_surface = pygame.Surface((self.scr_width, self.scr_height), pygame.SRCALPHA)
        
    def draw(self):
        """Draw all features to the screen.
        """
        # Clear window and draw window background 
        self.window.fill(self.BG_FILL)

        # Draw board background
        self.window.blit(self.board_surface, (0, 0))
        self.board_surface.fill(self.BG_FILL)
        
        if self.render_game:
            _, left_buf, top_buf, _ = win_utils.get_board_buffers()
            self.board_surface.fill((self.BG_FILL, self.BG_FILL, self.BG_FILL, bc.BACKGROUND_ALPHA), pygame.Rect(left_buf, top_buf, self.scr_width, self.scr_height))

            # Draw board grids 
            win_utils.draw_grids(self.board_surface)

            # Draw all pieces
            self.game.draw_pieces(self.board_surface, GameSettings.show_queue)

        # Draw fps counter
        if GameSettings.show_fps:
            fps_string = self.font.render(
                str(int(self.game.last_fps_recorded)),
                True, 
                self.FPS_COLOUR
            )
            
            self.board_surface.blit(fps_string, (self.scr_width - (win_utils.get_grid_size() * 3), win_utils.get_grid_size() / 2))
        
        # Draw score
        if GameSettings.show_score:
            score_string = self.font.render(
                str(f"score:  {self.game.score}"),
                True, 
                self.SCORE_COLOUR
            )
            
            # Draw back 2 back counter
            b2b_string = self.font.render(
                str(f"B2B:  {self.game.b2b}"),
                True, 
                self.B2B_COLOUR
            )

            # Draw score
            self.board_surface.blit(score_string, ((win_utils.get_grid_size()), win_utils.get_grid_size() / 2))

            # Draw back 2 back counter
            self.board_surface.blit(b2b_string, ((win_utils.get_grid_size()), win_utils.get_grid_size() * 2))

        # Update window
        pygame.display.flip()
