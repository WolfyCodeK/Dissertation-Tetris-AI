import numpy as np
import board_utils as bu
import pieces
from tetramino import Tetramino
import random
from custom_game_exceptions import PiecePlacementError

class PieceController():
    EMPTY_PIECE_PID = 'E'
    FLOOR_PIECE_PID = 'F'
    WALL_PIECE_PID = 'W'
    NONE_PIECE_TYPES = [EMPTY_PIECE_PID, FLOOR_PIECE_PID, WALL_PIECE_PID]

    # All the available pieces to the piece controller
    PIECE_CLASS_LIST = [pieces.ZPiece, pieces.SPiece, pieces.LPiece, pieces.JPiece, pieces.TPiece, pieces.IPiece, pieces.OPiece]

    NUM_OF_PIECES = len(PIECE_CLASS_LIST)

    piece_queue = []
    
    NUM_OF_QUEUE_TO_DRAW = 5
    
    PIECE_PID_LIST  = []
    for i in range(len(PIECE_CLASS_LIST)):
                PIECE_PID_LIST.append(PIECE_CLASS_LIST[i].PID)
    
    BLOCKING_PIECE_TYPES = PIECE_PID_LIST.copy()
    BLOCKING_PIECE_TYPES.append(FLOOR_PIECE_PID)
    BLOCKING_PIECE_TYPES.append(WALL_PIECE_PID)
    
    COLOUR_PID_DICT = {}
    for i in range(len(PIECE_CLASS_LIST)):
        COLOUR_PID_DICT[PIECE_PID_LIST[i]] = PIECE_CLASS_LIST[i].COLOUR
    
    def __init__(self) -> None:
        self.restart_board()
        
    def _init_board_state(self):
        # Initialise board state to be empty
        self.board_state = np.full(shape=(bu.BOARD_STATE_HEIGHT + bu.FLOOR_SIZE, bu.BOARD_STATE_WIDTH), fill_value=self.EMPTY_PIECE_PID)
            
        # Set wall pieces
        # Right wall
        for x in range(bu.BOARD_RIGHT_WALL, bu.BOARD_STATE_WIDTH):
            for y in range(len(self.board_state)):
                self.board_state[y][x] = self.WALL_PIECE_PID
            
        # Left wall
        for x in range(bu.BOARD_LEFT_WALL):
            for y in range(len(self.board_state)):
                self.board_state[y][x] = self.WALL_PIECE_PID
                
        # Set floor pieces
        for i in range(bu.FLOOR_SIZE):
            self.board_state[bu.BOARD_STATE_HEIGHT + i] = self.FLOOR_PIECE_PID
    
    def restart_board(self):
        self._init_board_state()
        self._init_piece_queue()
        self.new_piece()
        
        self.held_piece = None
        self.new_hold_available = True
        
    def draw_deactivated_pieces(self, surface):
        for y in range(len(self.board_state)):
            for x in range(len(self.board_state[0])):
                if (self.board_state[y][x] not in self.NONE_PIECE_TYPES):
                    bu.draw_rect(x, y, self.COLOUR_PID_DICT[self.board_state[y][x]], surface)
            
    def draw_current_piece(self, surface):
        self.current_piece.draw(surface)
        
    def draw_ghost_pieces(self, surface):
        self.current_piece.draw_ghost_pieces(surface, self._calculate_max_drop_height())
        
    def draw_held_piece(self, surface):
        x_adjust = - 2
        y_adjust = 6
        
        if (self.held_piece != None):
            self.held_piece.reset_shape()
            
            for i in range(len(self.held_piece.shape)):
                if (self.held_piece.pid == 'O'):
                    x_adjust += 1
                if (self.held_piece.pid == 'I'):
                    y_adjust -= 1
                bu.draw_rect(self.held_piece.shape[i][0] + x_adjust, self.held_piece.shape[i][1] + y_adjust, self.held_piece.colour, surface)
                
                x_adjust = -2
                y_adjust = 6
                
    def draw_queued_pieces(self, surface):
        x_adjust = 15
        y_adjust = 6

        for i in range(self.NUM_OF_QUEUE_TO_DRAW):
            # Get piece in queue
            piece = self.piece_queue[i]
            piece.reset_shape()
            
            for j in range(len(piece.shape)):
                if (piece.pid == 'O'):
                    x_adjust += 1
                if (piece.pid == 'I'):
                    y_adjust -= 1
                bu.draw_rect(piece.shape[j][0] + x_adjust, piece.shape[j][1] + y_adjust + (i * 3), piece.colour, surface)
                
                x_adjust = 15
                y_adjust = 6
        pass
        
    def gravity_drop_piece(self) -> bool:
        """Attempts to drop a tetramino piece down by one row.

        Returns:
            bool: True if the piece was successfully dropped down one row
        """
        if (not self._piece_is_vertically_blocked(self.board_state, self.current_piece, 1)):
            self.current_piece.set_y_pos(self.current_piece.y_pos + 1)
            return True
        else:
            return False
        
    def _calculate_max_drop_height(self) -> int:
        piece_dropped = False
        drop_amount = 1
        
        while (not piece_dropped):
            if (not self._piece_is_vertically_blocked(self.board_state, self.current_piece, drop_amount)):
                drop_amount += 1
            else:
                piece_dropped = True
                
        return drop_amount - 1
        
    def hard_drop_piece(self) -> None:
        self.current_piece.set_y_pos(self.current_piece.y_pos + self._calculate_max_drop_height())
        
    def shift_piece_horizontally(self, x_move):
        if (not self._piece_is_horizontally_blocked(self.board_state, self.current_piece, x_move)):
            self.current_piece.set_x_pos(self.current_piece.x_pos + x_move)
            
    def rotate_piece(self, clockwise: bool) -> None:    
        is_IPiece = self.current_piece.pid == 'I'
        
        self.current_piece.rotate_piece(clockwise, is_IPiece)
            
        self._move_occupying_square_if_blocked()
            
    def deactivate_piece(self) -> None:
        self.current_piece.active = False
        self._place_piece(self.board_state, self.current_piece)
    
    def new_piece(self) -> None:
        self.current_piece = self.piece_queue.pop(0)
        self.add_piece_to_queue()
    
    def create_piece_bags(self):
        self.first_bag_numbers = list(range(0, self.NUM_OF_PIECES))
        random.shuffle(self.first_bag_numbers)
        self.second_bag_numbers = list(range(0, self.NUM_OF_PIECES))
        random.shuffle(self.second_bag_numbers)
        
    def add_piece_to_queue(self):
        if (len(self.second_bag_numbers) <= 0):
            self.second_bag_numbers = list(range(0, self.NUM_OF_PIECES))
            random.shuffle(self.second_bag_numbers)
            
        piece_num = self.first_bag_numbers.pop(0)
        self.first_bag_numbers.append(self.second_bag_numbers.pop(0))

        self.piece_queue.append(self.PIECE_CLASS_LIST[piece_num]())

    def _init_piece_queue(self):
        self.create_piece_bags()
        
        for i in range(self.NUM_OF_PIECES):
            piece_num = self.first_bag_numbers[i]
            self.piece_queue.append(self.PIECE_CLASS_LIST[piece_num]())
        
    def perform_line_clears(self) -> int:
        lines_cleared = 0
        
        for y in range(len(self.board_state)):
            column_count = 0 
            
            for x in range(bu.BOARD_STATE_WIDTH):
                if self.board_state[y][x] not in self.NONE_PIECE_TYPES:
                    column_count += 1
                    
            if column_count >= bu.BOARD_COLUMNS:    
                lines_cleared += 1   
                
                for y2 in range(y, 1, -1):
                    self.board_state[y2] = self.board_state[y2 - 1]
                    
        return lines_cleared
                    
    def check_game_over(self) -> bool:
        for y in range(bu.BOARD_STATE_HEIGHT_BUFFER):
            if any(pid in self.PIECE_PID_LIST for pid in self.board_state[y].tolist()):
                return True
    
    def _move_occupying_square_if_blocked(self):
        piece = self.current_piece
        x_pos = piece.x_pos
        y_pos = piece.y_pos
        
        shift_amount = 1
        
        if (piece.pid == 'I'):
            shift_amount = 2
        
        for i in range(len(piece.minos)):
            if (piece.minos[i][1] == y_pos + 1) and (self.board_state[piece.minos[i][1]][piece.minos[i][0]] in self.BLOCKING_PIECE_TYPES):
                self.current_piece.set_y_pos(self.current_piece.y_pos - shift_amount)
                
            if (piece.minos[i][0] == x_pos + 1) and (self.board_state[piece.minos[i][1]][piece.minos[i][0]] in self.BLOCKING_PIECE_TYPES):
                self.current_piece.set_x_pos(self.current_piece.x_pos - shift_amount)
                
            if (piece.minos[i][0] == x_pos - 1) and (self.board_state[piece.minos[i][1]][piece.minos[i][0]] in self.BLOCKING_PIECE_TYPES):
                self.current_piece.set_x_pos(self.current_piece.x_pos + shift_amount)
                
    def _piece_is_vertically_blocked(self, board_state, piece: Tetramino, y_move) -> bool:
        blocked = False

        for i in range(len(piece.minos)):
            piece_pos = piece.minos[i][1] + y_move
            
            # Check the piece isnt going to hit the floor
            if (piece_pos != self.FLOOR_PIECE_PID):
                # Check if piece is in the board
                if (piece.minos[i][1] + 1 >= 0):
                    pos_state = board_state[piece_pos][piece.minos[i][0]]
                    
                    # If there is a piece there then the position is blocked
                    if (pos_state != self.EMPTY_PIECE_PID):  
                        blocked = True
            else:
                blocked = True
                    
        return blocked
    
    def _piece_is_horizontally_blocked(self, board_state, piece: Tetramino, x_move) -> bool:
        blocked = False
        
        for i in range(len(piece.minos)):
            piece_pos = piece.minos[i][0] + x_move
            
            # Check for right input
            if (x_move > 0):
                if (piece_pos + x_move <= bu.BOARD_RIGHT_WALL):
                    if (board_state[piece.minos[i][1]][piece_pos] != self.EMPTY_PIECE_PID):
                        blocked = True
                else:
                    blocked = True
            
            # Check for left input
            if (x_move < 0):
                if (piece_pos + x_move >= bu.BOARD_LEFT_WALL - 1):
                    if (board_state[piece.minos[i][1]][piece_pos] != self.EMPTY_PIECE_PID):
                        blocked = True
                else:
                    blocked = True          
            
        return blocked

    def _place_piece(self, board_state, piece: Tetramino):
        for i in range(len(piece.minos)):
            y = piece.minos[i][1]
            x = piece.minos[i][0]
            
            if (board_state[y][x] not in self.BLOCKING_PIECE_TYPES):
                board_state[piece.minos[i][1]][piece.minos[i][0]] = piece.pid
            else:
                raise PiecePlacementError(x, y, piece.pid)
            
        self.new_hold_available = True
        
    def hold_piece(self):
        if (self.held_piece != None) and (self.new_hold_available):
            temp_piece = self.current_piece
            self.current_piece = self.held_piece
            self.held_piece = temp_piece
            
            self.new_hold_available = False
            
            self.held_piece.reset_pos()
            
        elif (self.held_piece == None):
            self.held_piece = self.current_piece
            self.new_piece()
            
            self.new_hold_available = False
            
            self.held_piece.reset_pos()