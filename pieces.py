import pygame

#get access to the sprites
import spritesheet_files.parser as parser

class Piece:
    def __init__(self, location, sprite, white = False):
        self._location = location
        self._sprite = parser.sprites[sprite + str(white)]

        #color will always be either white or black, like a boolean
        self._white = white

class Pawn(Piece):
    def __init__(self, location, white = False):
        Piece.__init__(self, location, 'pawn', white)

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