from numpy import array

THREE_WIDE_PIECE_ROTATION_TABLE = array([
    # Clockwise
    # Side Squares
    [
        # (0, -1)
        [1, 1],
        
        # (0, 1)
        [-1, -1],
        
        # (-1, 0)
        [1, -1],
        
        # (1, 0)
        [-1, 1]
    ],
    
    # Corner Squares
    [
        # (-1, -1)
        [2, 0],
        
        # (1, -1)
        [0, 2],
        
        # (1, 1)
        [-2, 0],
        
        # (-1, 1)
        [0, -2]
    ],
    
    # Anti-Clockwise
    # Side Squares
    [
        # (0, -1)
        [-1, 1],
        
        # (0, 1)
        [1, -1],
        
        # (-1, 0)
        [1, 1],
        
        # (1, 0)
        [-1, -1]
    ],
    
    # Corner Squares
    [
        # (-1, -1)
        [0, 2],
        
        # (1, -1)
        [-2, 0],
        
        # (1, 1)
        [0, -2],
        
        # (-1, 1)
        [2, 0]
    ],
])

IPIECE_ROTATION_TABLE = array([
    # Clockwise
    # State 0
    [
        [2, -1],
        [1, 0],
        [0, 1],
        [-1, 2]
    ],
    
    # State 1
    [
        [1, 2],
        [0, 1],
        [-1, 0],
        [-2, -1]
    ],
    
    #State 2
    [
        [1, -2],
        [0, -1],
        [-1, 0],
        [-2, 1]
    ],
    
    #State 3
    [
        [2, 1],
        [1, 0],
        [0, -1],
        [-1, -2]
    ],
    
    # Anti-Clockwise
    # State 0
    [
        [1, 2],
        [0, 1],
        [-1, 0],
        [-2, -1]
    ],
    
    # State 1
    [
        [-2, 1],
        [-1, 0],
        [0, -1],
        [1, -2]
    ],
    
    # State 2
    [
        [2, 1],
        [1, 0],
        [0, -1],
        [-1, -2]
    ],
    
    # State 3
    [
        [-1, 2],
        [0, 1],
        [1, 0],
        [2, -1]
    ]
])

THREE_WIDE_PIECE_KICK_TABLE = ([
    # State 0
    [
        [-1, 0],
        [-1, 1],
        [0, -2],
        [-1, -2]
    ],
    
    # State 1
    [
        [-1, 0],
        [-1, -1],
        [0, 2],
        [-1, 2]
    ],
    
    # State 2
    [
        [1, 0],
        [1, 1],
        [0, -2],
        [1, -2]
    ],
    
    # State 3
    [
        [1, 0],
        [1, -1],
        [0, 2],
        [1, 2]
    ]
])

IPIECE_KICK_TABLE = ([
    # Clockwise
    # State 0
    [
        [-2, 0],
        [1, 0],
        [-2, 1],
        [1, -2]  
    ],
    
    # State 1
    [
        [-1, 0],
        [2, 0],
        [-1, -2],
        [2, 1]  
    ],
    
    # State 2
    [
        [2, 0],
        [-1, 0],
        [2, -1],
        [-1, 2]  
    ],
    
    # State 3
    [
        [1, 0],
        [-2, 0],
        [1, 2],
        [-2, -1]  
    ],
    
    # Anti-clockwise
    # State 0
    [
        [-1, 0],
        [2, 0],
        [-1, -2],
        [2, 1]
    ],
    
    # State 1
    [
        [-2, 0],
        [1, 0],
        [-2, 1],
        [1, -2]
    ],
    
    # State 2
    [
        [1, 0],
        [-2, 0],
        [1, 2],
        [-2, -1]
    ],
    
    # State 3
    [
        [2, 0],
        [-1, 0],
        [2, -1],
        [-1, 2]
    ],
    
])