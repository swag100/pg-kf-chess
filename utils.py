#contains general functions for use in multiple files. makes things nice and organized!
import pygame

pygame.joystick.init()

TILE_SIZE=24
TILE_COUNT=8

#screen size variables
SCREEN_SIZE=(256,224)
SCREEN_ZOOM=3

def get_piece_at(pieces, location):
    for piece in pieces:
        if piece._location == location:
            return piece
        
def make_transparent_rect(size, color, alpha):
    surface=pygame.surface.Surface(size)
    surface.fill(color)
    surface.set_alpha(alpha) #make it half transparent for good looks, haha!!

    return surface

def get_joysticks():
    return [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]