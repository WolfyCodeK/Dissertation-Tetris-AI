import pieces
import numpy as np
import board_utils as bu
from tetramino import Tetramino
import tetramino_features as tf
import random

class PieceController():

    drop_speed = 30
    drop_time = 1 / drop_speed

    NUM_OF_PIECES = 5
    PIECE_DEACTIVATE_DELAY = drop_speed

    piece_numbers = list(range(0, NUM_OF_PIECES))
    bag_counter = 0
    
    def __init__(self) -> None:
        # Initialise board state to be empty
        self.board_state = np.full(shape=(int(bu.BOARD_ROWS + bu.pixel_to_grid_size(bu.DROP_HEIGHT)), bu.BOARD_COLUMNS), fill_value=tf.EMPTY_PIECE_PID)
        self.current_piece = self.__create_new_piece()
        
    def draw_board_state(self, board_surface):
        for y in range(len(self.board_state)):
            for x in range(len(self.board_state[0])):
                for i in range(len(tf.COLOUR_PID_LIST)):
                    if (self.board_state[y][x] == tf.COLOUR_PID_LIST[i][0]):
                        bu.draw_rect(x, y, tf.COLOUR_PID_LIST[i][1], board_surface)
                    
    def drop_piece(self) -> bool:
        """Attempts to drop a tetramino piece down by 1 or more rows.

        Returns:
            bool: True if the piece was successfully dropped down 1 or more rows
        """
        if ((self.current_piece.y_pos < bu.BOARD_ROWS) and (not self.__piece_is_vertically_blocked(self.board_state, self.current_piece))):
            self.current_piece.set_y_pos(self.current_piece.y_pos + 1)
            return True
        else:
            return False
            
    def draw_piece(self, board_surface):
        self.current_piece.draw(board_surface)
        
    def shift_piece_by_amount(self, x):
        if (not self.__piece_is_horizontally_blocked(self.board_state, self.current_piece, x)):
            self.current_piece.set_x_pos(self.current_piece.x_pos + x)
            
    def deactivate_piece(self) -> None:
        self.current_piece.active = False
        self.__place_piece(self.board_state, self.current_piece)
        self.current_piece = self.__create_new_piece()
    
    def __create_new_piece(self) -> Tetramino:
        if (self.bag_counter <= 0):
            random.shuffle(self.piece_numbers)
            self.bag_counter = self.NUM_OF_PIECES
            
        self.bag_counter -= 1
        
        piece_num = self.piece_numbers[self.bag_counter]
        
        random_piece = tf.PIECE_CLASS_LIST[piece_num]
        
        return random_piece()
    
    @staticmethod        
    def __place_piece(board_state, piece):
        for i in range(len(piece.occupying_squares)):
            board_state[piece.occupying_squares[i][1]][piece.occupying_squares[i][0]] = piece.pid
            
    @staticmethod
    def __piece_is_vertically_blocked(board_state, piece) -> bool:
        blocked = False

        for i in range(len(piece.occupying_squares)):
            # Check if piece is in the board
            if (piece.occupying_squares[i][1] + 1 >= 0):
                pos_state = board_state[piece.occupying_squares[i][1] + 1][piece.occupying_squares[i][0]]
                
                # If there is a piece there then the position is blocked
                if (pos_state != tf.EMPTY_PIECE_PID):  
                    blocked = True
                    
        return blocked
    
    @staticmethod
    def __piece_is_horizontally_blocked(board_state, piece, x) -> bool:
        blocked = False

        for i in range(len(piece.occupying_squares)):
            piece_pos = piece.occupying_squares[i][0] + x
            
            if (x > 0):
                if (piece_pos + x <= bu.BOARD_COLUMNS):
                    if (board_state[piece.occupying_squares[i][1]][piece.occupying_squares[i][0] + x] != tf.EMPTY_PIECE_PID):
                        blocked = True
                else:
                    blocked = True
            
            if (x < 0):
                if (piece_pos + x >= -1):
                    if (board_state[piece.occupying_squares[i][1]][piece.occupying_squares[i][0] + x] != tf.EMPTY_PIECE_PID):
                        blocked = True
                else:
                    blocked = True          
            
        return blocked