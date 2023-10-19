import pygame
from board.board import Board
from controllers.logic_controller import LogicController
from pieces.piece_controller import PieceController
from controllers.window_controller import WindowController
from game.game_states import GameStates


def main():
    # Pygame intial setup
    pygame.display.init()
    pygame.font.init()
    
    pygame.display.set_caption("Tetris - Pygame")

    # Set window icon
    tetris_icon = pygame.image.load("res/tetris-icon.png")
    pygame.display.set_icon(tetris_icon)

    # Create game board
    board = Board()

    # Create controllers for the game
    p_controller = PieceController(board)
    l_controller = LogicController(p_controller)
    w_controller = WindowController(l_controller)

    game_state = GameStates.INIT_STATE
    
    running = True
    
    while running:
        # Check if user has quit the window
        if (pygame.event.get(pygame.QUIT)):
            running = False
        
        match game_state:
            case GameStates.INIT_STATE:
                # Run any initialisation code here
                game_state = GameStates.UPDATE_TIME
            
            case GameStates.UPDATE_TIME:
                l_controller.update_delta_time()
                l_controller.increment_frames_passed()
                l_controller.update_fps_counter()
                game_state = GameStates.TAKE_INPUTS
                
            case GameStates.TAKE_INPUTS:
                l_controller.take_player_inputs(pygame.event.get())
                game_state = GameStates.RUN_LOGIC
                
            case GameStates.RUN_LOGIC:
                l_controller.run_timed_game_logic()
                game_state = GameStates.DRAW_GAME
                
            case GameStates.DRAW_GAME:
                w_controller.draw()
                game_state = GameStates.UPDATE_TIME