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

    def find_tiles_where_i_can_move(self, pieces):
        valid_places=[]

        #add every possible move into valid_places
        for offset in self._places_to_move:
            valid_places.append(
                (
                    self._location[0] + offset[0],
                    self._location[1] + offset[1]
                )
            )

        #remove any places that are taken up by a piece
        for piece in pieces:
            for place in valid_places:
                if piece._location == place:
                    valid_places.remove(place)
        
        return valid_places

    def draw(self, screen):
        #no need for a get method when you can access the variables directly like this
        #you can create a get method if you prefer, whatever makes more sense to you

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

class Knight(Piece):
    def __init__(self, location, white = False):
        Piece.__init__(self, location, 'knight', white)

class Bishop(Piece):
    def __init__(self, location, white = False):
        Piece.__init__(self, location, 'bishop', white)

class Rook(Piece):
    def __init__(self, location, white = False):
        Piece.__init__(self, location, 'rook', white)

class King(Piece):
    def __init__(self, location, white = False):
        Piece.__init__(self, location, 'king', white)

class Queen(Piece):
    def __init__(self, location, white = False):
        Piece.__init__(self, location, 'queen', white)