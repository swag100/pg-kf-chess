#objects for player cursors

import pygame
import utils

class Cursor:
    def __init__(self, joy, joystick):
        self._joystick=joystick
        self._joy=joy
        self._white=bool(joy % 2)

        self._sensitivity=6
        self._threshold=0.1

        self._position=[0,0]
        self._speed=[0,0]

        self._selection=None

    def handle_event(self, pieces, event, board_position=(0,0)):
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

        if event.type in [pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP]:
            if self._joy == event.joy:
                #the TILE coordinates that you're clicking on.
                #tricky to explain, just ask me about it if you don't understand
                #// is INTEGER division
                cursor_location=(int((self._position[0] - board_position[0]) // utils.TILE_SIZE), int((self._position[1] - board_position[1]) // utils.TILE_SIZE))

                if event.type == pygame.JOYBUTTONDOWN:
                    self._selection=utils.get_piece_at(pieces, cursor_location)

                    if self._selection and self._white != self._selection._white:
                        self._selection=None

                else:
                    if self._selection:
                        self._selection.move_to(pieces, cursor_location)

                    self._selection=None

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
        pygame.draw.circle(screen, (255,0,0) if self._white else (0,255,0), self._position, 4)