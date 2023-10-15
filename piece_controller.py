import numpy as np
import board_utils as bu
import pieces
import random

class PieceController():
    EMPTY_PIECE_PID = 'E'
    FLOOR_PIECE_PID = 'F'
    NONE_PIECE_TYPES = [EMPTY_PIECE_PID, FLOOR_PIECE_PID]

    # All the available pieces to the piece controller
    PIECE_CLASS_LIST = [pieces.ZPiece, pieces.SPiece, pieces.LPiece, pieces.JPiece, pieces.TPiece, pieces.IPiece, pieces.OPiece]

    NUM_OF_PIECES = len(PIECE_CLASS_LIST)
    PIECE_NUMBERS = list(range(0, NUM_OF_PIECES))
    
    PIECE_PID_LIST  = []
    for i in range(len(PIECE_CLASS_LIST)):
                PIECE_PID_LIST.append(PIECE_CLASS_LIST[i].PID)
    
    COLOUR_PID_DICT = {}
    for i in range(len(PIECE_CLASS_LIST)):
        COLOUR_PID_DICT[PIECE_PID_LIST[i]] = PIECE_CLASS_LIST[i].COLOUR
    
    bag_counter = 0
    
    def __init__(self) -> None:
        self.init_board_state()
        self.new_piece()
    
    def init_board_state(self):
        # Initialise board state to be empty
        self.board_state = np.full(shape=(bu.BOARD_STATE_HEIGHT + bu.FLOOR_SIZE, bu.BOARD_COLUMNS), fill_value=self.EMPTY_PIECE_PID)
        
        # Set floor pieces
        for i in range(bu.FLOOR_SIZE):
            self.board_state[bu.BOARD_STATE_HEIGHT + i] = self.FLOOR_PIECE_PID
    
    def restart_board(self):
        self.init_board_state()
        self.new_piece()
        
    def draw_deactivated_pieces(self, surface):
        for y in range(len(self.board_state)):
            for x in range(len(self.board_state[0])):
                if (self.board_state[y][x] not in self.NONE_PIECE_TYPES):
                    bu.draw_rect(x, y, self.COLOUR_PID_DICT[self.board_state[y][x]], surface)
            
    def draw_current_piece(self, surface):
        self.current_piece.draw(surface)
        
    def draw_ghost_pieces(self, surface):
        self.current_piece.draw_ghost_pieces(surface, self.calculate_max_drop_height())
        
    def gravity_drop_piece(self) -> bool:
        """Attempts to drop a tetramino piece down by one row.

        Returns:
            bool: True if the piece was successfully dropped down one row
        """
        if (not self.__piece_is_vertically_blocked(self.board_state, self.current_piece, 1)):
            self.current_piece.set_y_pos(self.current_piece.y_pos + 1)
            
            return True
        else:
            return False
        
    def calculate_max_drop_height(self):
        piece_dropped = False
        drop_amount = 1
        
        while (not piece_dropped):
            if (not self.__piece_is_vertically_blocked(self.board_state, self.current_piece, drop_amount)):
                drop_amount += 1
            else:
                piece_dropped = True
                return drop_amount - 1
        
    def hard_drop_piece(self):
        self.current_piece.set_y_pos(self.current_piece.y_pos + self.calculate_max_drop_height())
        
    def shift_piece_horizontally(self, x_move):
        if (not self.__piece_is_horizontally_blocked(self.board_state, self.current_piece, x_move)):
            self.current_piece.set_x_pos(self.current_piece.x_pos + x_move)
            
    def rotate_piece(self, clockwise):
        is_IPiece = not (self.current_piece.pid != 'I' and self.current_piece.pid != 'O')
        
        if (not is_IPiece):
            self.__rotate_direction(clockwise, is_IPiece)
        elif self.current_piece.pid == 'I':
            self.__rotate_direction(clockwise, is_IPiece)
                
    def __rotate_direction(self, clockwise, is_IPiece):
        if (clockwise == 1):
            self.current_piece.rotate_clockwise(is_IPiece)
        else:
            self.current_piece.rotate_anticlockwise(is_IPiece)
            
    def deactivate_piece(self) -> None:
        self.current_piece.active = False
        self.__place_piece(self.board_state, self.current_piece)
    
    def new_piece(self) -> None:
        if (self.bag_counter <= 0):
            random.shuffle(self.PIECE_NUMBERS)
            self.bag_counter = self.NUM_OF_PIECES
            
        self.bag_counter -= 1
        
        piece_num = self.PIECE_NUMBERS[self.bag_counter]

        self.current_piece = self.PIECE_CLASS_LIST[piece_num]() 
        
    def perform_line_clears(self):
        columns = len(self.board_state[0])

        for y in range(len(self.board_state)):
            column_count = 0 
            
            for x in range(columns):
                if self.board_state[y][x] not in self.NONE_PIECE_TYPES:
                    column_count += 1
                    
            if column_count >= columns:                    
                for y2 in range(y, 1, -1):
                    self.board_state[y2] = self.board_state[y2 - 1]
                    
    def check_game_over(self):
        for y in range(bu.BOARD_STATE_HEIGHT_BUFFER):
            if any(pid in self.PIECE_PID_LIST for pid in self.board_state[y].tolist()):
                return True
            
    def __piece_is_vertically_blocked(self, board_state, piece, y_move) -> bool:
        blocked = False

        for i in range(len(piece.occupying_squares)):
            piece_pos = piece.occupying_squares[i][1] + y_move
            
            # Check the piece isnt going to hit the floor
            if (piece_pos != self.FLOOR_PIECE_PID):
                # Check if piece is in the board
                if (piece.occupying_squares[i][1] + 1 >= 0):
                    pos_state = board_state[piece_pos][piece.occupying_squares[i][0]]
                    
                    # If there is a piece there then the position is blocked
                    if (pos_state != self.EMPTY_PIECE_PID):  
                        blocked = True
            else:
                blocked = True
                    
        return blocked
    
    def __piece_is_horizontally_blocked(self, board_state, piece, x_move) -> bool:
        blocked = False
        for i in range(len(piece.occupying_squares)):
            piece_pos = piece.occupying_squares[i][0] + x_move
            
            # Check for right input
            if (x_move > 0):
                if (piece_pos + x_move <= bu.BOARD_COLUMNS):
                    if (board_state[piece.occupying_squares[i][1]][piece_pos] != self.EMPTY_PIECE_PID):
                        blocked = True
                else:
                    blocked = True
            
            # Check for left input
            if (x_move < 0):
                if (piece_pos + x_move >= -1):
                    if (board_state[piece.occupying_squares[i][1]][piece_pos] != self.EMPTY_PIECE_PID):
                        blocked = True
                else:
                    blocked = True          
            
        return blocked

    def __place_piece(self, board_state, piece):
        for i in range(len(piece.occupying_squares)):
            board_state[piece.occupying_squares[i][1]][piece.occupying_squares[i][0]] = piece.pid