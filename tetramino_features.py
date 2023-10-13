import pieces

EMPTY_PIECE_PID = 'E'
PIECE_CLASS_LIST = [pieces.ZPiece, pieces.SPiece, pieces.LPiece, pieces.JPiece, pieces.TPiece]

COLOUR_PID_DICT = {}
for i in range(len(PIECE_CLASS_LIST)):
    COLOUR_PID_DICT[PIECE_CLASS_LIST[i].PID] = PIECE_CLASS_LIST[i].COLOUR