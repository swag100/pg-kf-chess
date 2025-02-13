#PARSER.PY

import pygame
import utils

#loads spritesheet image for sparsing
spritesheet=pygame.image.load("spritesheet_files/spritesheet.png")

#renamed so i can do piece_name + if the piece is white
sprite_names=[["pawnTrue", "knightTrue", "bishopTrue", "rookTrue", "kingTrue", "queenTrue"],
               ["pawnFalse", "knightFalse", "bishopFalse", "rookFalse", "kingFalse", "queenFalse"]]
               
#creating sprite dictionary
sprites={}

#sprite size
sprite_size=(21,21)

#filling sprite dictionary
for row in range(2):
    for col in range(6):
        surface=pygame.Surface(sprite_size, pygame.SRCALPHA)
        surface.blit(spritesheet, (-sprite_size[0]*(col), -sprite_size[1]*(row)))

        sprites[sprite_names[row][col]]=surface