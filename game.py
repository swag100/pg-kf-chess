#GAME.PY

#https://spheya.artstation.com/projects/QnaVO3 assets used for chess images.

import sys
import pygame
from utils import TILE_SIZE, TILE_COUNT, COLORS, BOARD_POSITION

#import all piece classes
from pieces import *
from cursor import Cursor

#starts a pygame module
pygame.init()

#https://www.pygame.org/docs/ref/joystick.html
joysticks=utils.get_joysticks()

cursors=[]

#creates a screen with given dimensions and sets caption
surface = pygame.surface.Surface(utils.SCREEN_SIZE)

screen = pygame.display.set_mode(tuple(axis * utils.SCREEN_ZOOM for axis in utils.SCREEN_SIZE))
pygame.display.set_caption("Chess")

#variable to control game loop
playing=True

#list that contains every piece object
pieces=[]

def board_setup():
    #create both rows of pawns with loops
    for color in range(2):
        for col in range(8):
            white = bool(color) #bool(0) == False; bool(1) == True

            #find which row to put our pawn, based on color
            row = 1
            if white: 
                row = 6

            pawn = Pawn( 
                (col, row), #location; each value goes from 0-7
                white #is it white?
            )

            pieces.append(pawn)
    #creates both sets of knights, both sets of bishops, and both sets of rooks
    for color in range(2):
        for col in range(2):
            white = bool(color) #bool(0) == False; bool(1) == True

            #find which row to put our pawn, based on color
            row = 0
            if white: 
                row = 7

            knight = Knight( 
                ((col+1)+(col*4), row), #location; each value goes from 0-7
                white #is it white?
            )
            bishop = Bishop( 
                ((col+2)+(col*2), row), #location; each value goes from 0-7
                white #is it white?
            )
            rook = Rook( 
                ((col)+(col*6), row), #location; each value goes from 0-7
                white #is it white?
            )

            pieces.append(knight)
            pieces.append(bishop)
            pieces.append(rook)
    #creates both kings and both queens
    for color in range(2):
        white = bool(color) #bool(0) == False; bool(1) == True

        #find which row to put our pawn, based on color
        row = 0
        if white: 
            row = 7

        king = King( 
            (4, row), #location; each value goes from 0-7
            white #is it white?
        )
        queen = Queen( 
            (3, row), #location; each value goes from 0-7
            white #is it white?
        )

        pieces.append(king)
        pieces.append(queen)

board_setup()

def cursor_setup():
    joysticks=utils.get_joysticks()
    
    for joystick in joysticks:
        already_has_cursor=False
        for cursor in cursors:
            if cursor._joystick == joystick:
                already_has_cursor=True

        if not already_has_cursor: 
            cursors.append(Cursor(joysticks.index(joystick) % 2, joystick))
        
    for cursor in cursors:
        if cursor._joystick not in joysticks:
            cursors.remove(cursor)

cursor_setup()

while playing: #no need to do playing==True; playing literally just is true
    for event in pygame.event.get():

        #ends the game on closure
        if event.type == pygame.QUIT:
            #this is going to be done whether you like it or not boy.
            pygame.quit()
            sys.exit()

        if event.type in [pygame.JOYDEVICEADDED, pygame.JOYDEVICEREMOVED]:
            cursor_setup()

        for cursor in cursors:
            cursor.handle_event(pieces, event, BOARD_POSITION)

    #UPDATE THINGS
    
    for piece in pieces:
        piece.update(BOARD_POSITION)
    for cursor in cursors:
        cursor.update()

    #DRAW!!

    #fill background
    surface.fill(COLORS[5])

    #draw board outline
    pygame.draw.rect(
        surface, 
        COLORS[4], 
        pygame.rect.Rect(
            BOARD_POSITION[0]-1, 
            BOARD_POSITION[1]-1, 
            TILE_SIZE*TILE_COUNT+2, 
            TILE_SIZE*TILE_COUNT+2,
        )
    )
    
    #draw checkered board
    for row in range(TILE_COUNT):
        for col in range(TILE_COUNT):
            pygame.draw.rect(
                surface, 
                COLORS[(col+row)%2], 
                pygame.rect.Rect(
                    (TILE_SIZE*col)+BOARD_POSITION[0], 
                    (TILE_SIZE*row)+BOARD_POSITION[1], 
                    TILE_SIZE, 
                    TILE_SIZE
                )
            )
        
    #draw selection tile
    for cursor in cursors:
        selection=cursor._selection

        if selection:
            #make it half transparent for good looks, haha!!    
            #selection_surface=utils.make_transparent_rect((TILE_SIZE,)*2, (0,255,0), 128)
            #surface.blit(selection_surface, ((selection._location[0] * TILE_SIZE) + board_position[0], (selection._location[1] * TILE_SIZE) + board_position[1]))

            #make it the top-most piece, so it doesnt appear behind any others!
            pieces.append(pieces.pop(pieces.index(selection)))

            #make it follow your mouse!
            selection_rect=selection._sprite.get_rect(topleft=selection._position)

            selection._position=[
                cursor._position[0] - (selection_rect.w / 2) - (selection._offset[0]),
                cursor._position[1] - (selection_rect.h / 2) + (selection._offset[1] / 2),
            ]
    
    #draw hover tile
    for cursor in cursors:
        if cursor._selection: continue

        cursor_location=((cursor._position[0]-BOARD_POSITION[0]) // TILE_SIZE, (cursor._position[1]-BOARD_POSITION[1]) // TILE_SIZE)

        cursor._hover=utils.get_piece_at(pieces, cursor_location)
        if cursor._hover:
            if cursor._white != cursor._hover._white:
                cursor._hover=None

            else:
                #make it half transparent for good looks, haha!!    
                #hover_surface=utils.make_transparent_rect((TILE_SIZE,)*2, (0,255,0), 64)
                #surface.blit(hover_surface, ((cursor._hover._location[0] * TILE_SIZE) + board_position[0], (cursor._hover._location[1] * TILE_SIZE) + board_position[1]))
        
                cursor._hover._lerp_position[1]-=1

    #sort by location y
    y_sorted_pieces=[]
    for piece in pieces:
        if len(y_sorted_pieces) <= 0:
            y_sorted_pieces.append(piece)
        else:
            if piece._location[1] < y_sorted_pieces[0]._location[1]:
                y_sorted_pieces.insert(0, piece)
            else:
                y_sorted_pieces.insert(1, piece)

    #draw pieces based off of their own positions, but sorted!
    for piece in y_sorted_pieces:

        for cursor in cursors:
            if piece == cursor._selection: #make this a variable of the piece class, right now only pawn has it.
                valid_move_places,valid_kill_places=piece.find_tiles_where_i_can_move(pieces)
                
                for place in valid_move_places:
                    pygame.draw.circle(
                        surface, 
                        COLORS[4], 
                        (
                            (place[0] * TILE_SIZE) + (TILE_SIZE / 2) + BOARD_POSITION[0], 
                            (place[1] * TILE_SIZE) + (TILE_SIZE / 2) + BOARD_POSITION[1]
                        ),
                        3
                    )
                    
                for place in valid_kill_places:
                    pygame.draw.circle(
                        surface, 
                        COLORS[4], 
                        (
                            (place[0] * TILE_SIZE) + (TILE_SIZE / 2) + BOARD_POSITION[0], 
                            (place[1] * TILE_SIZE) + (TILE_SIZE / 2) + BOARD_POSITION[1]
                        ), 
                        TILE_SIZE / 2, 
                        2
                    )

        #logic moved to pieces
        piece.draw(surface)
            
    for cursor in cursors:
        cursor.draw(surface)

    screen.blit(pygame.transform.scale_by(surface, utils.SCREEN_ZOOM),(0,0))
                
    #updates the screen
    pygame.display.update()

    #sets constant frame rate
    pygame.time.Clock().tick(60)