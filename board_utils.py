from pygame import draw, Rect

BOARD_ROWS = 20
BOARD_COLUMNS = 10

GRID_SIZE = 32
GRID_ALPHA = 150
BACKGROUND_ALPHA = 175
GRID_OUTLINE_WIDTH = 3
INNER_GRID_SUBTRACT_BUFFER = GRID_OUTLINE_WIDTH - 1

DROP_HEIGHT = 2
FLOOR_SIZE = 2

BOARD_STATE_HEIGHT = BOARD_ROWS + DROP_HEIGHT

BOARD_RIGHT_BUFFER = 6 * GRID_SIZE
BOARD_LEFT_BUFFER = 6 * GRID_SIZE
BOARD_TOP_BUFFER = 4 * GRID_SIZE
BOARD_BOTTOM_BUFFER = 4 * GRID_SIZE

BOARD_WIDTH = GRID_SIZE * BOARD_COLUMNS
BOARD_HEIGHT = GRID_SIZE * BOARD_ROWS

SCR_WIDTH = BOARD_WIDTH + BOARD_RIGHT_BUFFER + BOARD_LEFT_BUFFER
SCR_HEIGHT = BOARD_HEIGHT + BOARD_TOP_BUFFER + BOARD_BOTTOM_BUFFER

# Board Coordinate Definitions
TOP_LEFT_BOARD_CORNER = (BOARD_LEFT_BUFFER - 2, BOARD_TOP_BUFFER)
TOP_RIGHT_BOARD_CORNER = (BOARD_LEFT_BUFFER + BOARD_WIDTH + 1, BOARD_TOP_BUFFER)
BOTTOM_LEFT_BOARD_CORNER = (BOARD_LEFT_BUFFER - 2, BOARD_TOP_BUFFER + BOARD_HEIGHT + 1)
BOTTOM_RIGHT_BOARD_CORNER = (BOARD_LEFT_BUFFER + BOARD_WIDTH + 1, BOARD_TOP_BUFFER + BOARD_HEIGHT + 1)

def pixel_to_grid_size(x: int) -> int:
    """Converts pixel size to grid size e.g. 160 pixels to 5 squares, where grid size = 32.

    Args:
        x (int): Any length of pixels

    Returns:
        int: That length divided by the grid size
    """    
    return x / GRID_SIZE

def grid_to_pixel_length(x: int) -> int:
    """Converts grid size to pixel size e.g. 5 squares to 160 pixels, where grid size = 32.

    Args:
        x (int): Any number of squares

    Returns:
        int: That length multiplied by the grid size
    """
    return x * GRID_SIZE

def __draw_outer_grid(surface):
    # BOTTOM
    draw.line(surface, (255, 255, 255, 255), BOTTOM_LEFT_BOARD_CORNER, BOTTOM_RIGHT_BOARD_CORNER, width=GRID_OUTLINE_WIDTH)
    
    # LEFT
    draw.line(surface, (255, 255, 255, 255), TOP_LEFT_BOARD_CORNER, BOTTOM_LEFT_BOARD_CORNER, width=GRID_OUTLINE_WIDTH)
    
    # RIGHT
    draw.line(surface, (255, 255, 255, 255), TOP_RIGHT_BOARD_CORNER, BOTTOM_RIGHT_BOARD_CORNER, width=GRID_OUTLINE_WIDTH)
    
def __draw_inner_grid(surface):
    # VERTICAL LINES
    for x in range(1 * GRID_SIZE, BOARD_WIDTH, GRID_SIZE):
        draw.line(
            surface, 
            (255, 255, 255, GRID_ALPHA), 
            (x + BOARD_LEFT_BUFFER, BOARD_TOP_BUFFER), 
            (x + BOARD_LEFT_BUFFER, BOARD_HEIGHT + BOARD_TOP_BUFFER - INNER_GRID_SUBTRACT_BUFFER)
        )
    
    # HORIZONTAL LINES    
    for y in range(0, BOARD_HEIGHT, GRID_SIZE):
        draw.line(
            surface, 
            (255, 255, 255, GRID_ALPHA), 
            (BOARD_LEFT_BUFFER + INNER_GRID_SUBTRACT_BUFFER, y + BOARD_TOP_BUFFER), 
            (BOARD_WIDTH + BOARD_LEFT_BUFFER - INNER_GRID_SUBTRACT_BUFFER, y + BOARD_TOP_BUFFER)
        )

def draw_grids(surface, outer: bool = True, inner: bool = True) -> None:
    if (outer):
        __draw_outer_grid(surface)
        
    if (inner):
        __draw_inner_grid(surface)
    
def draw_rect(x, y, colour, surface):
    x = x + pixel_to_grid_size(BOARD_LEFT_BUFFER)
    y = y + pixel_to_grid_size(BOARD_TOP_BUFFER) - DROP_HEIGHT
    draw.rect(surface, colour, Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))