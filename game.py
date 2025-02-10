import sys
import pygame

#moved to pieces.py; not used in this file anymore
#import spritesheet_files.parser as parser 

#import all piece classes
from pieces import *

#starts a pygame module
pygame.init()

#screen size variables
screen_width=384
screen_height=384

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
is_white_turn=False

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

while playing: #no need to do playing==True; playing literally just is true
    for event in pygame.event.get():

        #ends the game on closure
        if event.type == pygame.QUIT:
            #this is going to be done whether you like it or not boy.
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT: #left click
                mouse_position=pygame.mouse.get_pos()

                #the TILE coordinates that you're clicking on.
                #tricky to explain, just ask me about it if you don't understand
                #// is INTEGER division
                mouse_location=(mouse_position[0] // 48, mouse_position[1] // 48)

                #is there a piece lying on this tile coordinate?
                for piece in pieces:
                    if piece._location == mouse_location:
                        #if we try to select a piece that isn't our color, remove our selection
                        if is_white_turn == piece._white:
                            selection=None

                            #break out of the loop so we dont loop through it anymore since we dont need to
                            break 

                        #if there was already a selection right here, we're trying to deselect the piece
                        if selection == piece:
                            selection=None
                        else:
                            selection=piece

                #print(mouse_location)

        #for debugging, just making sure is_white_turn works correctly
        #this will switch the turn to the other player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                is_white_turn = not is_white_turn
    
    #draw checkered board
    for row in range(8):
        for col in range(8):
            pygame.draw.rect(screen, colors[(col+row)%2], pygame.rect.Rect(48*col, 48*row, 48, 48))
        
    #draw selection tile
    if selection:
        selection_surface=pygame.surface.Surface((48, 48))
        selection_surface.fill((0,255,0))
        selection_surface.set_alpha(128) #make it half transparent for good looks, haha!!

        screen.blit(selection_surface, (selection._location[0] * 48, selection._location[1] * 48))

    #draw pieces based off of their own positions
    for piece in pieces:
        #logic moved to pieces
        piece.draw(screen)

        if piece == selection: #make this a variable of the piece class, right now only pawn has it.
            valid_places=piece.find_tiles_where_i_can_move(pieces)
            for place in valid_places:
                pygame.draw.circle(screen, (0, 0, 0), ((place[0] * 48) + 24, (place[1] * 48) + 24), 6)

    #updates the screen
    pygame.display.update()

    #sets constant frame rate
    pygame.time.Clock().tick(60)