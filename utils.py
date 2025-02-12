#contains general functions for use in multiple files. makes things nice and organized!
import pygame

def get_piece_at(pieces, location):
    for piece in pieces:
        if piece._location == location:
            return piece
        
def make_transparent_rect(size, color, alpha):
    surface=pygame.surface.Surface(size)
    surface.fill(color)
    surface.set_alpha(alpha) #make it half transparent for good looks, haha!!

    return surface