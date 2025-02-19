from collections import deque
import time
import numpy as np
from pieces.piece_type_id import PieceTypeID
import utils.board_constants as bc 
from controllers.game_controller import GameController

def get_placed_piece_max_height(game_controller: GameController):
    return game_controller.piece_manager.placed_piece_max_height

def get_board_state(game_controller: GameController):
    return game_controller.piece_manager.board.board_state

def get_bumpiness(game_controller: GameController):
    max_height_list = get_max_height_column_list(game_controller)
    
    # len(max_height_list) - 2, because we dont count well at index 9
    end_index = len(max_height_list) - 2
    
    total_bumpiness = 0
    
    for i, height in enumerate(max_height_list):
        bumpiness = 0
        
        if i > 0 and i < end_index:
            bumpiness += abs(height - max_height_list[i - 1])
            bumpiness += abs(height - max_height_list[i + 1])
        elif i == 0:
            bumpiness += abs(height - max_height_list[i + 1])
        elif i == end_index:
            bumpiness += abs(height - max_height_list[i - 1])
            
        total_bumpiness += bumpiness
        
    return total_bumpiness
    
def does_I_dependency_exist(game_controller: GameController):
    pass
    
def does_none_central_I_piece_exist(game_controller: GameController):
    pass

def get_max_height_column_list(game_controller: GameController):    
    board_state = get_board_state(game_controller)
    
    max_height_list = []
    
    # Horizontal loop
    for i in range(bc.BOARD_COLUMNS):
        column = board_state[:, i]
        
        peak_found = False
        
        # Vertical loop
        for j in bc.BOARD_HEIGHT_RANGE_INCR:
            if (column[j] > 0):
                max_height_list.append(bc.BOARD_HEIGHT - j)
                peak_found = True
                break
            
        if (peak_found == False):
            max_height_list.append(0) 
    
    return max_height_list

def get_column_heights(game_controller: GameController) -> list:
    max_height_column_list = get_max_height_column_list(game_controller)
    
    max_height_column_list.pop()
    
    return max_height_column_list

def get_max_piece_height_on_board(game_controller: GameController):
    return max(get_max_height_column_list(game_controller))

def get_min_height_column_list(game_controller: GameController):
    board_state = get_board_state(game_controller)
    
    min_height_list = []
    
    # Horizontal loop
    for i in range(bc.BOARD_COLUMNS):
        column = board_state[:, i]
        
        min_found = False
        
        # Vertical loop
        for j in bc.BOARD_HEIGHT_RANGE_INCR:
            if (column[j] > 0):
                min_height_list.append(bc.BOARD_HEIGHT - j)
                min_found = True
                break
            
        if (min_found == False):
            min_height_list.append(0) 
    
    return min_height_list

def get_min_piece_height_on_board(game_controller: GameController):
    return min(get_min_height_column_list(game_controller))

def get_first_gap_list(game_controller: GameController):
    board_state = get_board_state(game_controller)
    
    first_gap_list = []
    
    # Horizontal loop
    for i in range(bc.BOARD_COLUMNS):
        column = board_state[:, i]
        
        # Vertical loop
        for j in range(bc.BOARD_HEIGHT - 1, 0, -1):
            if (column[j] == 0):
                first_gap_list.append((bc.BOARD_HEIGHT - 1) - j)
                break
    
    return first_gap_list

def get_first_gap_list_excluding_well(game_controller: GameController):
    first_gap_list = get_first_gap_list(game_controller)
    
    first_gap_list.pop()
    
    return first_gap_list

def get_num_of_top_gaps(game_controller: GameController):
    board_state = get_board_state(game_controller)
    
    max_height_list = get_max_height_column_list(game_controller)
    gaps = 0
    
    # Horizontal loop
    for i in range(bc.BOARD_COLUMNS):
        column = board_state[:, i]
        left_wall = False
        right_wall = False
        
        if i > 0:
            left = board_state[:, i - 1]
        else:
            left_wall = True
            
        if i < bc.BOARD_COLUMNS - 1:   
            right = board_state[:, i + 1]
        else:
            right_wall = True

        # Vertical loop
        for j in range(bc.BOARD_HEIGHT - max_height_list[i], bc.BOARD_HEIGHT):
            if (column[j] == 0) and (column[j - 1] > 0) and ((not((left_wall == True) or (left[j] > 0))) or (not((right_wall == True) or (right[j] > 0)))):
                gaps += 1
                
    return gaps      

def get_num_of_full_gaps(game_controller: GameController):
    board_state = get_board_state(game_controller)
    
    max_height = get_max_piece_height_on_board(game_controller)
    gaps = 0
    
    # Vertical loop
    for i in range(bc.BOARD_HEIGHT - max_height, bc.BOARD_HEIGHT):
        middle_row = board_state[i, :]
        
        if (i > 0):
            top_row = board_state[i - 1, :]
        else:
            top_row = None
        
        # Horizontal loop
        for j in range(bc.BOARD_COLUMNS):
            if (middle_row[j] == 0) and (top_row[j] > 0) and ((j == 0) or (middle_row[j - 1] > 0)):
                if (j == bc.BOARD_COLUMNS - 1) or (middle_row[j + 1] > 0):
                    added_gaps = 1
                else:
                    check_finished = False
                    
                    added_gaps = 1
                    
                    while not check_finished:
                        j += 1
                        
                        if (j < bc.BOARD_COLUMNS):
                            next_pos_right = middle_row[j] == 0
                            next_pos_top = top_row[j] > 0
                            
                            if next_pos_right and not next_pos_top:
                                check_finished = True
                                added_gaps = 0
                                
                            elif next_pos_right and next_pos_top:
                                added_gaps += 1
                                
                            elif not next_pos_right:
                                check_finished = True
                        else:
                            check_finished = True
                            
                gaps += added_gaps

    return gaps      

def does_board_have_gaps(game_controller: GameController):
    return (get_num_of_full_gaps(game_controller) + get_num_of_top_gaps(game_controller)) > 0

def is_tetris_ready(game_controller: GameController):
    max_list = get_column_heights(game_controller)
    
    board = get_board_state(game_controller)
    
    if len(np.argwhere(board[:, bc.BOARD_COLUMNS - 1])) != 0:
        if bc.BOARD_HEIGHT - min(np.argwhere(board[:, bc.BOARD_COLUMNS - 1])) <= (get_max_piece_height_on_board(game_controller) - 4):
            return not any([height < 4 for height in max_list])
        else:
            return False
    return not any([height < 4 for height in max_list])

def is_well_invalid(game_controller: GameController):
    board_state = get_board_state(game_controller)
    
    invalid = False
    
    # Vertical loop
    for i in bc.BOARD_HEIGHT_RANGE_INCR:
        last_column_id = board_state[i, bc.BOARD_COLUMNS - 1]
        
        if last_column_id != PieceTypeID.I_PIECE and last_column_id != PieceTypeID.EMPTY:
            invalid = True
        elif last_column_id == PieceTypeID.I_PIECE and not is_tetris_ready(game_controller): 
            invalid = True
        
    return invalid

def get_board_height_difference_excluding_well(game_controller: GameController):
    return get_max_piece_height_on_board(game_controller) - get_min_gap_height_excluding_well(game_controller)

def has_exceeded_max_board_height_difference(game_controller: GameController, max_height):
    return (get_max_piece_height_on_board(game_controller) - get_min_gap_height_excluding_well(game_controller)) > max_height

def get_truncated_piece_queue(game_controller: GameController, first_n_pieces):
    return game_controller.piece_manager.piece_queue.get_truncated_piece_queue(first_n_pieces)

def get_current_piece_id(game_controller: GameController) -> int:
    return game_controller.piece_manager.current_piece.id

def get_piece_value_bounds(game_controller: GameController):
    return game_controller.piece_manager.board.EMPTY_PIECE_ID, len(PieceTypeID)

def get_held_piece_id(game_controller: GameController) -> int:
    return game_controller.piece_manager.piece_holder.held_piece.id if game_controller.piece_manager.piece_holder.held_piece is not None else 0

def get_min_gap_height_excluding_well(game_controller: GameController) -> int:
    return min(get_first_gap_list_excluding_well(game_controller))

def get_max_gap_height_excluding_well(game_controller: GameController) -> int:
    return max(get_first_gap_list_excluding_well(game_controller))

def get_relative_board_max_heights_excluding_well(game_controller: GameController, max_height: int) -> np.ndarray:
    max_height_list = get_column_heights(game_controller)
    
    relative_max_heights = np.array(max_height_list) - min(max_height_list)
    
    max_height_value = max(relative_max_heights)
    
    if max_height_value > max_height:
        top_down_rel_max_heights = []
        
        for height in relative_max_heights:
            top_down_rel_max_heights.append(max_height - (max_height_value - height))
            
        relative_max_heights = np.clip(top_down_rel_max_heights, a_min = 0, a_max = max_height) 
    return relative_max_heights

def get_relative_column_heights(game_controller: GameController, target_max_height: int) -> np.ndarray:
    current_column_heights = get_column_heights(game_controller)
    
    # Subtract the lowest column height from all columns
    current_relative_column_heights = current_column_heights - min(current_column_heights)
    
    current_relative_max_column_height = max(current_relative_column_heights)
    
    # Reduce all columns height to match the target height
    if current_relative_max_column_height > target_max_height:
        target_column_heights = deque()
        
        for height in current_relative_column_heights:
            # Calculate column height relative to the target max height
            target_column_heights.append(target_max_height - (current_relative_max_column_height - height))
            
        # Convert to numpy array and change any negative heights to zero
        target_column_heights = np.clip(target_column_heights, a_min = 0, a_max = target_max_height) 
    
    return target_column_heights


