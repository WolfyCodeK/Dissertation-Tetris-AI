import numpy as np
import utils.board_constants as bc

import utils.window_utils as win_utils
from pieces.i_piece import IPiece
from pieces.o_piece import OPiece
from pieces.three_wide_pieces import (JPiece, LPiece, SPiece, TPiece, ZPiece)

class Board():
    # All the available pieces to the piece controller
    PIECE_LIST = [ZPiece, SPiece, JPiece, LPiece, TPiece, IPiece, OPiece]
    
    EMPTY_PIECE_ID = 0
    
    # Dict of (ID, colour) pairs for all pieces
    PIECE_COLOUR_DICT = {}
    for i in range(len(PIECE_LIST)):
        PIECE_COLOUR_DICT[PIECE_LIST[i].ID] = PIECE_LIST[i].COLOUR
        
    def __init__(self) -> None:
        self.INITIAL_BOARD_STATE = self._init_board_state()
        self.reset_board_state()
    
    def draw(self, surface):
        for y in bc.BOARD_HEIGHT_RANGE:
            for x in range(bc.BOARD_WIDTH):
                id = self.board_state[y][x]
                
                if (id in Board.PIECE_COLOUR_DICT.keys()):
                    win_utils.draw_rect(x, y, self.PIECE_COLOUR_DICT[id], surface)
                    
    def check_game_over(self):
        for y in range(bc.BOARD_HEIGHT_BUFFER):
            if any(id in self.PIECE_COLOUR_DICT.keys() for id in self.board_state[y].tolist()):
                return True
    
    def reset_board_state(self):
        self.board_state = self.INITIAL_BOARD_STATE.copy()
    
    def _init_board_state(self):
        return np.full(shape=(bc.BOARD_HEIGHT, bc.BOARD_WIDTH), fill_value=self.EMPTY_PIECE_ID)
    
    def get_minimal_board_state(self):
        min_board_state = self.board_state.copy()
        
        min_board_state = np.delete(min_board_state, range(0, bc.BOARD_HEIGHT_BUFFER), axis=0)
        
        return min_board_state