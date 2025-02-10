#PIECES.PY
import pygame

#get access to the sprites
import spritesheet_files.parser as parser

class Piece:
    def __init__(self, location, sprite, white = False):
        self._location = location
        self._sprite = parser.sprites[sprite + str(white)]

        #color will always be either white or black, like a boolean
        self._white = white

        #list of offsets applied to the piece's current location
        self._places_to_move=[]
        self._places_to_kill=[]

    def find_tiles_where_i_can_move(self, pieces):
        move_places=[]

        #add every possible move into valid_places
        for offset in self._places_to_move:
            move_places.append(
                (
                    self._location[0] + offset[0],
                    self._location[1] + (offset[1])*((self._white*2)-1)
                )
            )

        #remove any places that are taken up by a piece, along with everything past it
        piece_found=False
        for piece in pieces:
            for place in move_places:
                if piece_found:
                    move_places.remove(place)
                    break

                if piece._location == place:
                    piece_found=True
                
        return move_places

    def find_tiles_where_i_can_kill(self, pieces):
        invalid_places=[]

        #add every possible move into valid_places
        for offset in self._places_to_kill:
            invalid_places.append(
                (
                    self._location[0] + offset[0],
                    self._location[1] + (offset[1])*((self._white*2)-1)
                )
            )

        kill_places=[]

        #remove any places that do not contain a piece
        for piece in pieces:
            if piece._location in invalid_places:
                if piece._white != self._white:
                    kill_places.append(piece._location)
                
        return kill_places

    def draw(self, screen):
        piece_position = [
            (self._location[0] * 48) + 3,
            (self._location[1] * 48) + 3,
        ]

        screen.blit(self._sprite, piece_position)

class Pawn(Piece):
    def __init__(self, location, white = False):
        Piece.__init__(self, location, 'pawn', white)

        self._places_to_move=[
            (0, -1),
            (0, -2)
        ]

        self._places_to_kill=[
            (-1, -1),
            (1, -1)
        ]

class Knight(Piece):
    def __init__(self, location, white = False):
        Piece.__init__(self, location, 'knight', white)

        self._places_to_move=[
            (-2, -1),
            (-2, 1),
            (-1, 2),
            (-1, -2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1)
        ]

        self._places_to_kill=self._places_to_move

class Bishop(Piece):
    def __init__(self, location, white = False):
        Piece.__init__(self, location, 'bishop', white)

class Rook(Piece):
    def __init__(self, location, white = False):
        Piece.__init__(self, location, 'rook', white)

class King(Piece):
    def __init__(self, location, white = False):
        Piece.__init__(self, location, 'king', white)

        self._places_to_kill=self._places_to_move

class Queen(Piece):
    def __init__(self, location, white = False):
        Piece.__init__(self, location, 'queen', white)