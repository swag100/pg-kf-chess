#GAME.PY

#https://spheya.artstation.com/projects/QnaVO3 assets used for chess images.

import sys
import pygame
from utils import TILE_SIZE, TILE_COUNT

#import all piece classes
from pieces import *
from cursor import Cursor

#starts a pygame module
pygame.init()

#https://www.pygame.org/docs/ref/joystick.html
joysticks=utils.get_joysticks()
print(joysticks)

cursors=[]

#screen size variables
screen_width=TILE_SIZE*TILE_COUNT
screen_height=TILE_SIZE*TILE_COUNT

#creates a screen with given dimensions and sets caption
screen = pygame.display.set_mode((screen_width, screen_width))
pygame.display.set_caption("Chess")

#color code constants
WHITE=(255, 255, 255)
BLACK=(127, 159, 184)

#color list
colors=[WHITE, BLACK]

#variable to control game loop
playing=True

#list that contains every piece object
pieces=[]

#variable that keeps track of the players selection, if any. will either be a piece object or None.
selection=None

#i don't know why but it works starting as false
is_white_turn=True

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

for joystick in joysticks:
    cursors.append(Cursor(joysticks, joystick, bool(joysticks.index(joystick) % 2)))

while playing: #no need to do playing==True; playing literally just is true
    for event in pygame.event.get():

        #ends the game on closure
        if event.type == pygame.QUIT:
            #this is going to be done whether you like it or not boy.
            pygame.quit()
            sys.exit()

        if event.type in [pygame.JOYDEVICEADDED, pygame.JOYDEVICEREMOVED]:
            joysticks=utils.get_joysticks()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT: #left click
                mouse_position=pygame.mouse.get_pos()

                """
                if selection and is_white_turn != selection._white:
                    selection=None
                """

        for cursor in cursors:
            cursor.handle_event(pieces, event)
    
    #draw checkered board
    for row in range(TILE_COUNT):
        for col in range(TILE_COUNT):
            pygame.draw.rect(screen, colors[(col+row)%2], pygame.rect.Rect(TILE_SIZE*col, TILE_SIZE*row, TILE_SIZE, TILE_SIZE))
        
    #draw selection tile
    if selection:
        #make it half transparent for good looks, haha!!    
        selection_surface=utils.make_transparent_rect((TILE_SIZE,)*2, (0,255,0), 128)

        screen.blit(selection_surface, (selection._location[0] * TILE_SIZE, selection._location[1] * TILE_SIZE))

    #draw pieces based off of their own positions
    for piece in pieces:
        #logic moved to pieces
        piece.draw(screen)

        if piece == selection: #make this a variable of the piece class, right now only pawn has it.
            valid_move_places,valid_kill_places=piece.find_tiles_where_i_can_move(pieces)
            
            for place in valid_move_places:
                pygame.draw.circle(
                    screen, 
                    (0, 0, 0), 
                    (
                        (place[0] * TILE_SIZE) + (TILE_SIZE / 2), 
                        (place[1] * TILE_SIZE) + (TILE_SIZE / 2)
                    ),
                    6
                )
                
            for place in valid_kill_places:
                pygame.draw.circle(
                    screen, 
                    (0, 0, 0), 
                    (
                        (place[0] * TILE_SIZE) + (TILE_SIZE / 2), 
                        (place[1] * TILE_SIZE) + (TILE_SIZE / 2)
                    ), 
                    TILE_SIZE / 2, 
                    4
                )
        
        if isinstance(piece, King) and piece._is_in_check:
            check_surface=utils.make_transparent_rect((TILE_SIZE,)*2, (255,0,0), 128)

            screen.blit(check_surface, (piece._location[0] * TILE_SIZE, piece._location[1] * TILE_SIZE))
            
    for cursor in cursors:
        cursor.update()
        cursor.draw(screen)
                
    #updates the screen
    pygame.display.update()

    #sets constant frame rate
    pygame.time.Clock().tick(60)