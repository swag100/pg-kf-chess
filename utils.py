#contains general functions for use in multiple files. makes things nice and organized!
import pygame

pygame.joystick.init()

FRAME_RATE=60

TILE_SIZE=16
TILE_COUNT=8

PIECE_MAX_MOVE = TILE_COUNT - 1

#screen size variables
SCREEN_SIZE=(192,192)
SCREEN_ZOOM=4

#where we draw the entire board and pieces
BOARD_POSITION=(32,32)

PIECES=['pawn', 'knight', 'bishop', 'rook', 'king', 'queen']

#color list
COLORS=[
    (217, 216, 157), #white
    (130, 76, 76), #black
    (227, 128, 74), #DARK white
    (77, 51, 59), #DARK black
    (45, 30, 34), #outline color
    (83, 149, 170), #background color
]

def position_to_location(position, offset=(0,0)):
    return (
        (position[0] - offset[0]) // TILE_SIZE,
        (position[1] - offset[1]) // TILE_SIZE
    )

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

#https://stackoverflow.com/questions/42821442/
def fill(surface, color):
    w, h = surface.get_size()
    r, g, b = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))

def draw_board(surface):
    #draw board outline
    pygame.draw.rect(
        surface, 
        COLORS[4], 
        pygame.rect.Rect(
            BOARD_POSITION[0]-1, 
            BOARD_POSITION[1]-1, 
            TILE_SIZE*TILE_COUNT+2, 
            TILE_SIZE*TILE_COUNT+2,
        )
    )
    
    #draw checkered board
    for row in range(TILE_COUNT):
        for col in range(TILE_COUNT):
            pygame.draw.rect(
                surface, 
                COLORS[(col+row)%2], 
                pygame.rect.Rect(
                    (TILE_SIZE*col)+BOARD_POSITION[0], 
                    (TILE_SIZE*row)+BOARD_POSITION[1], 
                    TILE_SIZE, 
                    TILE_SIZE
                )
            )

def get_white_string(white):
    return 'white' if white else 'black'