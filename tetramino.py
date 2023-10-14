import board_utils as bu
import numpy as np

class Tetramino:
    def __init__(self, pid: chr, x: int, colour: tuple, shape: np.ndarray, large_rotation: bool = False) -> None:
        self.pid = pid
        self.x_pos = x
        self.y_pos = bu.PIECE_START_HEIGHT
        self.colour = colour
        self.shape = shape
        self.occupying_squares = shape.copy()
        
        self.update_occupying_squares()
        
        # The rotational space for 3x3 Tetraminos
        self.rotational_space = np.array([
            [[0,0], [1,0], [2,0]],
            [[0,1], [1,1], [2,1]],
            [[0,2], [1,2], [2,2]]
        ])
        
        # The rotational space for 4x4 Tetraminos
        if (large_rotation):
            self.rotational_space = np.array([
                [[0,0], [1,0], [2,0], [3,0]],
                [[0,1], [1,1], [2,1], [3,1]],
                [[0,2], [1,2], [2,2], [3,2]],
                [[0,2], [1,2], [2,2], [3,3]]
            ])
        
        self.active = True
    
    def draw(self, surface):
        for i in range(len(self.occupying_squares)):
            bu.draw_rect(self.occupying_squares[i][0], self.occupying_squares[i][1], self.colour, surface)
    
    def update_occupying_squares(self):      
        for i in range(len(self.shape)):
            self.occupying_squares[i][0] = self.shape[i][0] + self.x_pos
            self.occupying_squares[i][1] = self.shape[i][1] + self.y_pos
    
    def set_x_pos(self, x: int) -> None:
        self.x_pos = x
        self.update_occupying_squares()
    
    def set_y_pos(self, y: int) -> None:
        self.y_pos = y
        self.update_occupying_squares()
    
    def rotate_anticlockwise(self):
        pass
    
    def rotate_clockwise(self):
        print(self.rotational_space)