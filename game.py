#GAME.PY

import sys
import pygame
from utils import *

#import all piece classes
from pieces import *
from cursor import Cursor

#starts a pygame module
pygame.init()

#https://www.pygame.org/docs/ref/joystick.html
joysticks=get_joysticks()

cursors=[]

#creates a screen with given dimensions and sets caption
surface = pygame.surface.Surface(SCREEN_SIZE)

screen = pygame.display.set_mode(tuple(axis * SCREEN_ZOOM for axis in SCREEN_SIZE))
pygame.display.set_caption("Chess")
pygame.mouse.set_visible(False)

#variable to control game loop
playing=True

#winner: who won the game?
winner=None

def board_setup(pieces):
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

    return pieces

#list that contains every piece object
pieces = board_setup([])

def cursor_setup():
    joysticks=get_joysticks()
    
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
    
    if len(joysticks) <= 0:
        cursors.append(Cursor(0,None))

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

        if event.type == pygame.USEREVENT:
            winner=event.winning_color

            playing=False

        for cursor in cursors:
            cursor.handle_event(pieces, event)

    #UPDATE THINGS
    
    for piece in pieces:
        piece.update(BOARD_POSITION)
    for cursor in cursors:
        cursor.update()

    #DRAW!!

    #fill background
    surface.fill(get_color(5))

    draw_board(surface)

    #sort by location y
    y_sorted_pieces = sorted(pieces, key=lambda x: x._location[1])
        
    #draw selection tile
    for cursor in cursors:
        selection=cursor._selection

        if selection and selection in y_sorted_pieces:
            #make it the top-most piece, so it doesnt appear behind any others!
            y_sorted_pieces.append(y_sorted_pieces.pop(y_sorted_pieces.index(selection)))

            #make it follow your mouse!
            #save offset of when you first grab the piece.

            selection._position=[
                cursor._position[0] - cursor._piece_offset[0],
                cursor._position[1] - cursor._piece_offset[1]
            ]
    
    #draw hover tile
    for cursor in cursors:
        if cursor._selection: continue

        collided_piece=None

        for piece in y_sorted_pieces:
            if piece._hitbox.collidepoint(*cursor._position):
                collided_piece=piece

        cursor._hover=collided_piece

        if cursor._hover and cursor._hover._cool_down_time_elapsed <= cursor._hover._cool_down_time:
            cursor._hover=None

        if cursor._hover and cursor._white != cursor._hover._white:
            cursor._hover=None

        if cursor._hover:
            cursor._hover._lerp_position[1]-=PIECE_HOVER_RAISE * PIECE_DRAG

    #draw pieces based off of their own positions, but sorted!
    for piece in y_sorted_pieces:

        for cursor in cursors:
            if piece == cursor._selection: #make this a variable of the piece class, right now only pawn has it.
                valid_move_places,valid_kill_places=piece.find_tiles_where_i_can_move(pieces)
                
                for place in valid_move_places:
                    pygame.draw.circle(
                        surface, 
                        get_color(OUTLINE), 
                        (
                            (place[0] * TILE_SIZE) + (TILE_SIZE / 2) + BOARD_POSITION[0], 
                            (place[1] * TILE_SIZE) + (TILE_SIZE / 2) + BOARD_POSITION[1]
                        ),
                        3
                    )
                    
                for place in valid_kill_places:
                    pygame.draw.circle(
                        surface, 
                        get_color(OUTLINE), 
                        (
                            (place[0] * TILE_SIZE) + (TILE_SIZE / 2) + BOARD_POSITION[0], 
                            (place[1] * TILE_SIZE) + (TILE_SIZE / 2) + BOARD_POSITION[1]
                        ), 
                        TILE_SIZE / 2, 
                        #2
                    )

    for piece in y_sorted_pieces:
        #logic moved to pieces
        piece.draw(surface)
            
    for cursor in cursors:
        cursor.draw(surface)

    screen.blit(pygame.transform.scale_by(surface, SCREEN_ZOOM),(0,0))
                
    #updates the screen
    pygame.display.update()

    #sets constant frame rate
    pygame.time.Clock().tick(FRAME_RATE)

#create winner text surface, along with outlines
my_font = pygame.font.Font('fonts/PixelOperator8-Bold.ttf', 8)
text_surface = my_font.render(get_white_string(winner).title() + ' won!', False, get_color(not winner))

while not playing: #this will last until you close the window
    for event in pygame.event.get():

        #ends the game on closure
        if event.type == pygame.QUIT:
            #this is going to be done whether you like it or not boy.
            pygame.quit()
            sys.exit()

        if event.type in [pygame.JOYDEVICEADDED, pygame.JOYDEVICEREMOVED]:
            cursor_setup()
    
    #DRAW!!

    #fill background
    surface.fill(get_color(winner))

    surface.blit(text_surface, text_surface.get_rect(center=[x // 2 for x in SCREEN_SIZE]))

    screen.blit(pygame.transform.scale_by(surface, SCREEN_ZOOM),(0,0))
                
    #updates the screen
    pygame.display.update()

    #sets constant frame rate
    pygame.time.Clock().tick(FRAME_RATE)