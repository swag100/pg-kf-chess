#CURSOR.PY

#objects for player cursors

import pygame
import utils
from spritesheet import Parser

class Cursor:
    def __init__(self, joy, joystick):
        self._joystick=joystick
        self._joy=joy
        self._white=bool(joy % 2)

        self._sensitivity=3
        self._threshold=0.2

        self._position=[x // 2 for x in utils.SCREEN_SIZE]
        self._position[1] += utils.TILE_SIZE * ((self._white * 2) - 1) - (utils.TILE_SIZE / 2)

        self._speed=[0,0]

        self._selection=None
        self._hover=None

        #visual instance variables!
        self._parser=Parser("images/cursor.png",(16,16))
        self._sprites = self._parser.get_sprites(["idle", "grab"])
        self._sprite = self._parser.assemble_sprite(self._sprites["idle"],self._white)
        self._piece_offset=(0,0)
    
    def grab(self):

        self._sprite = self._parser.assemble_sprite(self._sprites["grab"],self._white)

        self._selection=self._hover

        if self._selection:
            self._piece_offset=(
                self._position[0] - self._hover._hitbox.x - self._selection._offset[0],
                self._position[1] - self._hover._hitbox.y - (self._selection._offset[1] / 2)
            )

        if self._selection:
            if self._white != self._selection._white:
                self._selection=None
                
        if self._selection:
            if self._selection._cool_down_time_elapsed <= self._selection._cool_down_time:
                self._selection=None

    def let_go(self, pieces):
        self._sprite = self._parser.assemble_sprite(self._sprites["idle"],self._white)

        if self._selection:
            #find the tile that the bottom of the sprite is at
            midbottom=list(self._selection._hitbox.midbottom)
            midbottom[1]-=4

            bottom_of_sprite_location=utils.position_to_location(midbottom, utils.BOARD_POSITION)

            self._selection.move_to(pieces, bottom_of_sprite_location)

        self._selection=None

    def handle_event(self, pieces, event):
        if self._joystick:
            if event.type == pygame.JOYAXISMOTION:
                if self._joy == event.joy:
                    axis_x, axis_y = (self._joystick.get_axis(0), self._joystick.get_axis(1))

                    if abs(axis_x) > self._threshold:
                        self._speed[0] = self._sensitivity * axis_x
                    else:
                        self._speed[0]=0
                    if abs(axis_y) > self._threshold:
                        self._speed[1] = self._sensitivity * axis_y
                    else:
                        self._speed[1]=0
                
                    if event.axis in [pygame.CONTROLLER_AXIS_TRIGGERLEFT, pygame.CONTROLLER_AXIS_TRIGGERRIGHT]:
                        if event.value > self._threshold:
                            if not self._selection:
                                self.grab()
                        else:
                            self.let_go(pieces)

        else:
            if event.type == pygame.MOUSEMOTION:
                self._position=[x // utils.SCREEN_ZOOM for x in event.pos]

        if event.type in [pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            if self._joystick:
                if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]: return
                if self._joy != event.joy: return

            if event.type in [pygame.JOYBUTTONDOWN, pygame.MOUSEBUTTONDOWN]:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        self._white=not self._white

                        return
                
                self.grab()
            else:
                self.let_go(pieces)

    def update(self):
        self._position[0] += self._speed[0]
        self._position[1] += self._speed[1]

        #Prevent cursor from going out of bounds
        for i in range(len(self._position)):
            axis=self._position[i]

            if axis > utils.SCREEN_SIZE[i]:
                self._position[i]=utils.SCREEN_SIZE[i]
            if axis < 0:
                self._position[i]=0

    def draw(self, screen):
        #pygame.draw.circle(screen, (255,0,0) if self._white else (0,255,0), self._position, 4)

        screen.blit(self._sprite, (self._position[0] - 7, self._position[1] - 1))