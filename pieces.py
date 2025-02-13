#PIECES.PY
import utils
from math import ceil

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

        #visual instance variables
        self._position=[axis*utils.TILE_SIZE for axis in self._location]
        self._lerp_position=self._position
        self._offset=(0,0)

        #count of moves. really just for the pawn
        self._moves=0

    def __str__(self):
        return f'{type(self).__name__} {self._location} {'white' if self._white else 'black'}'

    def move_to(self, pieces, new_location):
        move_tiles,kill_tiles=self.find_tiles_where_i_can_move(pieces)

        for place in move_tiles + kill_tiles:
            if place == new_location:
                if place in kill_tiles:
                    pieces.remove(utils.get_piece_at(pieces, place))

                self._location=place

                #putting it here cause im lazy
                if isinstance(self, Pawn):
                    self._places_to_move={
                        (0, -1): 1, #direction: amount
                    }

                    y=self._location[1]

                    if y > 6 or y < 1:
                        pieces.append(Queen(self._location, self._white))
                        pieces.remove(self)
    
    def find_tiles_where_i_can_move(self, pieces):
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
                        out_of_bounds=False
                        for axis in new_place:
                            if not 0 <= axis < utils.TILE_COUNT:
                                out_of_bounds=True

                        if not out_of_bounds:
                            move_places.append(new_place)

        return move_places, kill_places
    
    def update(self, board_position=(0,0)):
        self._lerp_position[0] += ceil((self._position[0] - self._lerp_position[0]) * 0.25)
        self._lerp_position[1] += ceil((self._position[1] - self._lerp_position[1]) * 0.25)

        self._position = [
            (self._location[0] * utils.TILE_SIZE) + board_position[0] + self._offset[0],
            (self._location[1] * utils.TILE_SIZE) + board_position[1] + self._offset[1],
        ]

    def draw(self, screen):
        screen.blit(self._sprite, self._lerp_position)

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

    def find_tiles_where_i_can_move(self, pieces):
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
                out_of_bounds=False
                for axis in new_place:
                    if not 0 <= axis < utils.TILE_COUNT:
                        out_of_bounds=True

                if not out_of_bounds:
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

        self._places_to_kill=self._places_to_move

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