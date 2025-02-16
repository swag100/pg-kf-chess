#SPRITESHEET.PY

import pygame
from utils import *

class Parser:
    def __init__(self, spritesheet_path, sprite_size):
        #loads spritesheet image for sparsing
        self._spritesheet=pygame.image.load(spritesheet_path)

        self._sprite_size=sprite_size
    
    def get_sprites(self, sprite_names):
        sprites={}

        spritesheet_size=self._spritesheet.get_size()

        #filling sprite dictionary
        for col in range(spritesheet_size[0]//self._sprite_size[0]):
            sprites[sprite_names[col]]=[]
            for row in range(spritesheet_size[1]//self._sprite_size[1]):
                surface=pygame.Surface(self._sprite_size, pygame.SRCALPHA)
                surface.blit(self._spritesheet, (-self._sprite_size[0]*(col), -self._sprite_size[1]*(row)))

                sprites[sprite_names[col]].append(surface)

        return sprites
        
    def assemble_sprite(self, sprite_layers, white):
        final_sprite=pygame.surface.Surface(sprite_layers[0].get_size(), pygame.SRCALPHA)

        #find correct color
        fill_colors=[
            get_color(OUTLINE),
            get_color(int(not white)),
            get_color(int(not white)+2),
        ]

        for i in range(len(sprite_layers)):
            surface=sprite_layers[i]
            fill(surface, fill_colors[i])
            final_sprite.blit(surface, (0,0))

        return final_sprite