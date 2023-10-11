import numpy as np
import board_utils as bu
from tetramino import Tetramino
import tretramino_features as tf

class ZPiece(Tetramino):
    def __init__(self, board_surface) -> None:
        super().__init__(
            tf.Z_PIECE_START_X, 
            tf.Z_PIECE_START_Y, 
            tf.Z_PIECE_COLOUR, 
            board_surface
        )
        
        self.__update_occupying_squares(self.x_pos, self.y_pos)
    
    def set_x_pos(self, x: int) -> None:
        self.x_pos = x
        self.__update_occupying_squares(self.x_pos, self.y_pos)
    
    def set_y_pos(self, y: int) -> None:
        self.y_pos = y
        self.__update_occupying_squares(self.x_pos, self.y_pos)
    
    def __update_occupying_squares(self, x, y):    
        self.occupying_squares = np.array([[x, y], [x + 1, y], [x, y - 1], [x - 1, y - 1]])
    
    