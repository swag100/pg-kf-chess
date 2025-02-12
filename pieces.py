#PIECES.PY
import pygame
import utils

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
        self._places_to_kill=self._places_to_move

        #count of moves. really just for the pawn
        self._moves=0

    def __str__(self):
        return f'{type(self).__name__} {self._location} {'white' if self._white else 'black'}'

    def move_to(self, pieces, new_location):
        piece_moved=False

        move_tiles,kill_tiles=self.find_tiles_where_i_can_move(pieces)

        for place in move_tiles + kill_tiles:
            if place == new_location:
                if place in kill_tiles:
                    pieces.remove(utils.get_piece_at(pieces, place))

                self._location=place
                piece_moved=True

        return piece_moved

    #find a better name for this function
    def find_tiles(self, pieces):
        move_places=[]
        kill_places=[]

        if isinstance(self._places_to_move, dict):
            for offset, length in self._places_to_move.items():
                for i in range(length):
                    new_place=(
                        self._location[0] + offset[0] * (i + 1),
                        self._location[1] + (offset[1]*((self._white*2)-1) * (i + 1))
                    )

                    new_piece=utils.get_piece_at(pieces, new_place)
                    if new_piece:
                        if new_piece._white != self._white:
                            kill_places.append(new_place)

                        break
                    else:

                        move_places.append(new_place)
    
        return move_places, kill_places
    
    def find_tiles_where_i_can_move(self, pieces):
        move_places, kill_places=self.find_tiles(pieces)

        #if board without this piece causes a check, that means any of its moves are invalid
        new_pieces=pieces.copy()
        new_pieces.remove(self)

        #WORK ON THIS TOMORROWW!!!
        """
        for piece in pieces:
            if not isinstance(piece, Knight):
                kill_tiles=piece.find_tiles(new_pieces)[1]

            #is any king in danger?
            for place in kill_tiles:
                king_piece=utils.get_piece_at(pieces, place)

                if isinstance(king_piece, King):
                    if place in move_places:
                        move_places.remove(place)
        """
                        
        return move_places, kill_places

    def draw(self, screen):
        piece_position = [
            (self._location[0] * 48) + 3,
            (self._location[1] * 48) + 3,
        ]

        screen.blit(self._sprite, piece_position)

class Pawn(Piece):
    def __init__(self, location, white = False):
        Piece.__init__(self, location, 'pawn', white)

        self._places_to_move={
            (0, -1): 2 #direction: amount
        }

        self._places_to_kill=[
            (-1, -1),
            (1, -1)
        ]

    def find_tiles_where_i_can_move(self, pieces):
        move_places=super().find_tiles_where_i_can_move(pieces)[0]

        kill_places=[]

        #add every possible move into valid_places
        for offset in self._places_to_kill:
            new_place=(
                self._location[0] + offset[0],
                self._location[1] + (offset[1])*((self._white*2)-1)
            )
            
            piece=utils.get_piece_at(pieces, new_place)
            if piece and piece._white != self._white:
                kill_places.append(new_place)

        return move_places, kill_places

    def move_to(self, pieces, new_location):
        piece_moved=super().move_to(pieces, new_location)
    
        if piece_moved:
            self._places_to_move={
                (0, -1): 1, #direction: amount
            }

            y=self._location[1]

            if y > 6 or y < 1:
                pieces.append(Queen(self._location, self._white))
                pieces.remove(self)

        return piece_moved
        
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

    def find_tiles(self, pieces):
        move_places=[]
        kill_places=[]

        #add every possible move into valid_places
        for offset in self._places_to_move:
            new_place=(
                self._location[0] + offset[0],
                self._location[1] + (offset[1])*((self._white*2)-1)
            )

            piece=utils.get_piece_at(pieces, new_place)
            if piece:
                if piece._white != self._white:
                    kill_places.append(new_place)
            else:
                move_places.append(new_place)

        return move_places, kill_places

class Bishop(Piece):
    def __init__(self, location, white = False):
        Piece.__init__(self, location, 'bishop', white)

        self._places_to_move={
            (-1, -1): 7, #direction: amount
            (1, -1): 7,
            (-1, 1): 7,
            (1, 1): 7
        }

        self._places_to_kill=self._places_to_move

class Rook(Piece):
    def __init__(self, location, white = False):
        Piece.__init__(self, location, 'rook', white)

        self._places_to_move={
            (0, -1): 7, #direction: amount
            (0, 1): 7,
            (-1, 0): 7,
            (1, 0): 7
        }

        self._places_to_kill=self._places_to_move

class King(Piece):
    def __init__(self, location, white = False):
        Piece.__init__(self, location, 'king', white)

        self._places_to_move={
            (-1, -1): 1, #direction: amount
            (1, -1): 1,
            (-1, 1): 1,
            (1, 1): 1,
            (0, -1): 1, #direction: amount
            (0, 1): 1,
            (-1, 0): 1,
            (1, 0): 1
        }

        self._is_in_check=False

        self._places_to_kill=self._places_to_move
    
    def find_tiles_where_i_can_move(self, pieces):
        move_places, kill_places=super().find_tiles_where_i_can_move(pieces)

        #if i move, and im in the killplace of any other piece, DONT ALLOW THAT MOVE!
        for place in move_places:
            for piece in pieces:
                if piece._white != self._white:
                    bad_places=piece.find_tiles(pieces)[0]

                    if place in bad_places:
                        if place in move_places:
                            move_places.remove(place)
                

        return move_places, kill_places

class Queen(Piece):
    def __init__(self, location, white = False):
        Piece.__init__(self, location, 'queen', white)

        self._places_to_move={
            (-1, -1): 7, #direction: amount
            (1, -1): 7,
            (-1, 1): 7,
            (1, 1): 7,
            (0, -1): 7, #direction: amount
            (0, 1): 7,
            (-1, 0): 7,
            (1, 0): 7
        }

        self._places_to_kill=self._places_to_move