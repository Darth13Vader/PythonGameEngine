import pygame
from pygame.locals import *
from GameEngine import PyGameEngine

class Camera:
    def __init__(self, engine: PyGameEngine, x=0, y=0):
        self.pos_x = x
        self.pos_y = y

        self.engine = engine

        self.keys_left = [K_a]
        self.keys_right = [K_d]
        self.keys_up = [K_w]
        self.keys_down = [K_s]
        
        self.moving_left  = False
        self.moving_right = False
        self.moving_up    = False
        self.moving_down  = False
        
        self.move_coeff = 15

    def get_position(self):
        return self.pos_x, self.pos_y

    def look_at_block(self, x, y):
        screen_w, screen_h = self.engine.screen_w, self.engine.screen_h
        blocks_in_width = screen_w // self.engine.block_height
        blocks_in_height = screen_h // self.engine.block_height
        left_border = (x - blocks_in_width // 2) * self.engine.block_height
        up_border = (y + blocks_in_height // 2) * self.engine.block_height
        self.pos_x = -left_border
        self.pos_y = up_border

    def update(self):
        for key in self.engine.input.pressedKeys:
            if key in self.keys_left:
                self.moving_left = True
            elif key in self.keys_right:
                self.moving_right = True
            elif key in self.keys_up:
                self.moving_up = True
            elif key in self.keys_down:
                self.moving_down = True
        for key in self.engine.input.unpressedKeys:
            if key in self.keys_left:
                self.moving_left = False
            elif key in self.keys_right:
                self.moving_right = False
            elif key in self.keys_up:
                self.moving_up = False
            elif key in self.keys_down:
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