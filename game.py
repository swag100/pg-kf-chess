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

while playing: #no need to do playing==True; playing literally just is true
    for event in pygame.event.get():

        #ends the game on closure
        if event.type == pygame.QUIT:
            exit()
    
    #draw checkered board
    for row in range(8):
        for col in range(8):
            pygame.draw.rect(screen, colors[(col+row)%2], pygame.rect.Rect(48*col, 48*row, 48, 48))

    """
    count=0
    for key in parser.sprites.keys():
        screen.blit(parser.sprites[key], ((48*count)+3, (48*count)+3))
        count+=1
    """
    #draw pieces based off of their own positions
    for piece in pieces:
        #no need for a get method when you can access the variables directly like this
        #you can create a get method if you prefer, whatever makes more sense to you

        piece_position = [
            (piece._location[0] * 48) + 3,
            (piece._location[1] * 48) + 3,
        ]

        screen.blit(piece._sprite, piece_position)
        

    #updates the screen
    pygame.display.update()

    #sets constant frame rate
    pygame.time.Clock().tick(60)