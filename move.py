class Move():
    def __init__(self, piece: Piece, new_pos_x: int, new_pos_y: int):
        self.piece = piece
        self.new_pos_x = new_pos_x
        self.new_pos_y = new_pos_y