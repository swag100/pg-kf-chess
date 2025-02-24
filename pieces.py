#PIECES.PY

import pygame
from utils import *

#get access to the sprites
from spritesheet import Parser

class Piece:
    def __init__(self, location, sprite, white = False):
        self._location = location

        #color will always be either white or black, like a boolean
        self._white = white

        #list of offsets applied to the piece's current location
        self._places_to_move=[]
        self._places_to_kill=self._places_to_move

        #visual instance variables
        self._offset=[0, -12]
        self._position = [
            (self._location[0] * TILE_SIZE) + BOARD_POSITION[0] + self._offset[0],
            (self._location[1] * TILE_SIZE) + BOARD_POSITION[1] + self._offset[1],
        ]
        self._lerp_position=self._position

        #sprite
        self._parser=Parser("images/pieces.png",(16,24))
        self._sprites = self._parser.get_sprites(PIECES)
        self._piece_sprite = self._parser.assemble_sprite(self._sprites[sprite],self._white)
        self._sprite=self._piece_sprite

        #count of moves. really just for the pawn
        self._moves=0

        #WOOOO KUNG FU CHESS!
        self._cool_down_time=5
        self._cool_down_time_elapsed=self._cool_down_time

        #where the cursor can detect the piece is
        self._hitbox=self.get_hitbox()

    def get_hitbox(self):
        hitbox=self._sprite.get_bounding_rect()
        
        on_cool_down=self._cool_down_time_elapsed<self._cool_down_time

        if not on_cool_down: hitbox.h+=PIECE_HOVER_RAISE
        hitbox.x+=self._position[0]
        hitbox.y+=self._position[1]-(PIECE_HOVER_RAISE if not on_cool_down else 0)

        return hitbox
        
    def mask_sprite(self, cur_sprite, mask_amount):
        final_sprite=cur_sprite.copy()

        sprite_rect=final_sprite.get_rect()
        sprite_bounding_rect=final_sprite.get_bounding_rect()

        mask_sprite_size=(
            sprite_rect.size[0],
            sprite_rect.size[1] - (sprite_bounding_rect.h * mask_amount)
        )

        mask_sprite=pygame.surface.Surface(mask_sprite_size, pygame.SRCALPHA)
        mask_sprite.blit(final_sprite, sprite_rect)
        fill(mask_sprite, get_color(OUTLINE))

        final_sprite.blit(mask_sprite, (0, 0))

        return final_sprite

    def move_to(self, pieces, new_location):
        move_tiles,kill_tiles=self.find_tiles_where_i_can_move(pieces)

        for place in move_tiles + kill_tiles:
            if place == new_location:
                piece=get_piece_at(pieces, place)

                if place in kill_tiles:
                    pieces.remove(piece)

                self._location=place

                #reset elapsed time
                self._cool_down_time_elapsed=0

                #putting it here cause im lazy
                if isinstance(self, Pawn):
                    self._places_to_move={
                        (0, -1): 1, #direction: amount
                    }

                    y=self._location[1]

                    if y > 6 or y < 1:
                        promoted_piece=Queen(self._location, self._white)
                        promoted_piece._cool_down_time_elapsed=0

                        pieces.append(promoted_piece)
                        pieces.remove(self)


                
                if isinstance(piece, King):
                    #post won event
                    event_to_post = pygame.event.Event(pygame.USEREVENT, {'winning_color': self._white})
                    pygame.event.post(event_to_post)
    
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

                    new_piece=get_piece_at(pieces, new_place)
                    if new_piece:
                        if new_piece._white != self._white:
                            kill_places.append(new_place)

                        break
                    else:
                        out_of_bounds=False
                        for axis in new_place:
                            if not 0 <= axis < TILE_COUNT:
                                out_of_bounds=True

                        if not out_of_bounds:
                            move_places.append(new_place)

        return move_places, kill_places
    
    def update(self, board_position=(0,0)):
        self._cool_down_time_elapsed+=(1/FRAME_RATE)

        self._lerp_position[0] += (self._position[0] - self._lerp_position[0]) * PIECE_DRAG
        self._lerp_position[1] += (self._position[1] - self._lerp_position[1]) * PIECE_DRAG

        #where the cursor can detect the piece is
        self._hitbox=self.get_hitbox()

        self._position = [
            (self._location[0] * TILE_SIZE) + board_position[0] + self._offset[0],
            (self._location[1] * TILE_SIZE) + board_position[1] + self._offset[1],
        ]

    def draw(self, screen):
        #pygame.draw.rect(screen, (255,0,0), self._hitbox)

        if self._cool_down_time_elapsed < self._cool_down_time:
            self._sprite = self.mask_sprite(self._piece_sprite, self._cool_down_time_elapsed / self._cool_down_time)
        else:
            self._sprite = self._piece_sprite

        screen.blit(self._sprite, [round(x) for x in self._lerp_position])

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
            
            piece=get_piece_at(pieces, new_place)
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

            piece=get_piece_at(pieces, new_place)
            if piece:
                if piece._white != self._white:
                    kill_places.append(new_place)
            else:
                out_of_bounds=False
                for axis in new_place:
                    if not 0 <= axis < TILE_COUNT:
                        out_of_bounds=True

                if not out_of_bounds:
                    move_places.append(new_place)

        return move_places, kill_places

class Bishop(Piece):
    def __init__(self, location, white = False):
        Piece.__init__(self, location, 'bishop', white)

        self._places_to_move={
            (-1, -1): PIECE_MAX_MOVE, #direction: amount
            (1, -1): PIECE_MAX_MOVE,
            (-1, 1): PIECE_MAX_MOVE,
            (1, 1): PIECE_MAX_MOVE
        }

        self._places_to_kill=self._places_to_move

class Rook(Piece):
    def __init__(self, location, white = False):
        Piece.__init__(self, location, 'rook', white)

        self._places_to_move={
            (0, -1): PIECE_MAX_MOVE, #direction: amount
            (0, 1): PIECE_MAX_MOVE,
            (-1, 0): PIECE_MAX_MOVE,
            (1, 0): PIECE_MAX_MOVE
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
            (-1, -1): PIECE_MAX_MOVE, #direction: amount
            (1, -1): PIECE_MAX_MOVE,
            (-1, 1): PIECE_MAX_MOVE,
            (1, 1): PIECE_MAX_MOVE,
            (0, -1): PIECE_MAX_MOVE, #direction: amount
            (0, 1): PIECE_MAX_MOVE,
            (-1, 0): PIECE_MAX_MOVE,
            (1, 0): PIECE_MAX_MOVE
        }

        self._places_to_kill=self._places_to_move