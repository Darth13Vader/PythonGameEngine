import pygame
from PythonGameEngine.GlobalVariables.Keys import *
from PythonGameEngine.GlobalVariables.Constants import *

class Camera:
    def __init__(self, screen, x=0, y=0):
        self.pos_x = x
        self.pos_y = y

        self.screen = screen

        self.keys_left = [KEY_A]
        self.keys_right = [KEY_D]
        self.keys_up = [KEY_W]
        self.keys_down = [KEY_S]
        
        self.moving_left  = False
        self.moving_right = False
        self.moving_up    = False
        self.moving_down  = False
        
        self.move_coeff = 15

    def get_position(self):
        return self.pos_x, self.pos_y

    def look_at_block(self, x, y):
        screen_w, screen_h = self.screen.get_width(), self.screen.get_height()

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in self.keys_left:
                    self.moving_left = True
                elif event.key in self.keys_right:
                    self.moving_right = True
                elif event.key in self.keys_up:
                    self.moving_up = True
                elif event.key in self.keys_down:
                    self.moving_down = True
            elif event.type == pygame.KEYUP:
                if event.key in self.keys_left:
                    self.moving_left = False
                elif event.key in self.keys_right:
                    self.moving_right = False
                elif event.key in self.keys_up:
                    self.moving_up = False
                elif event.key in self.keys_down:
                    self.moving_down = False

        cam_dx, cam_dy = 0, 0
        if self.moving_right:
            cam_dx -= self.move_coeff
        if self.moving_left:
            cam_dx += self.move_coeff
        if self.moving_up:
            cam_dy += self.move_coeff
        if self.moving_down:
            cam_dy -= self.move_coeff

        self.pos_x += cam_dx
        self.pos_y += cam_dy

        #print(self.pos_x, self.pos_y)