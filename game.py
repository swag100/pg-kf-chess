import pygame
import spritesheet_files.parser as parser

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

while playing == True:
    for event in pygame.event.get():

        #ends the game on closure
        if event.type == pygame.QUIT:
            exit()
    
    for row in range(8):
        for col in range(8):
            pygame.draw.rect(screen, colors[(col+row)%2], pygame.rect.Rect(48*col, 48*row, 48, 48))

    count=0
    for key in parser.sprites.keys():
        screen.blit(parser.sprites[key], ((48*count)+3, (48*count)+3))
        count+=1

    #updates the screen
    pygame.display.update()

    #sets constant frame rate
    pygame.time.Clock().tick(60)