#objects for player cursors

import pygame
import utils

class Cursor:
    def __init__(self, joysticks, joystick, white=False):
        self._joysticks=joysticks
        self._joystick=joystick
        self._joy=joysticks.index(joystick)
        self._white=white

        self._sensitivity=5
        self._threshold=0.2

        self._position=[0,0]
        self._speed=[0,0]

        self._selection=None

    def handle_event(self, pieces, event):
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

        if event.type == pygame.JOYBUTTONDOWN:
            if self._joy == event.joy:

                #the TILE coordinates that you're clicking on.
                #tricky to explain, just ask me about it if you don't understand
                #// is INTEGER division
                mouse_location=(self._position[0] // utils.TILE_SIZE, self._position[1] // utils.TILE_SIZE)

                if self._selection:
                    self._selection.move_to(pieces, mouse_location)
                
                old_selection=self._selection

                self._selection=utils.get_piece_at(pieces, mouse_location)

                if old_selection == self._selection:
                    self._selection=None
                
        if event.type == pygame.JOYBUTTONUP:
            if self._joy == event.joy:
                print(event)

    def update(self):
        self._position[0] += self._speed[0]
        self._position[1] += self._speed[1]

    def draw(self, screen):
        pygame.draw.rect(screen, (255,0,0) if self._white else (0,255,0), pygame.rect.Rect(*self._position, 24, 24))