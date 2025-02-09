import pygame

#loads spritesheet image for sparsing
spritesheet=pygame.image.load("spritesheet_files/spritesheet.png")

#creating list of sprite name for sprite dictionary
"""
sprite_names=[["w_pawn", "w_knight", "w_bishop", "w_rook", "w_king", "w_queen"],
               ["b_pawn", "b_knight", "b_bishop", "b_rook", "b_king", "b_queen"]]
"""
#renamed so i can do piece_name + if the piece is white
sprite_names=[["pawnTrue", "knightTrue", "bishopTrue", "rookTrue", "kingTrue", "queenTrue"],
               ["pawnFalse", "knightFalse", "bishopFalse", "rookFalse", "kingFalse", "queenFalse"]]
               
#creating sprite dictionary
sprites={}

#filling sprite dictionary
for row in range(2):
    for col in range(6):
        surface=pygame.Surface((21, 21), pygame.SRCALPHA)
        surface.blit(spritesheet, (-21*(col), -21*(row)))
        surface=pygame.transform.scale(surface, (42, 42))

        sprites[sprite_names[row][col]]=surface