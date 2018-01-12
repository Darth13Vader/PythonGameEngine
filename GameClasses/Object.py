import pygame


class Object:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def setup(self, screen, images):
        self.screen = screen
        self.images = images

    def update(self):
        # Method called one time per frame
        self.render_self()
        pass

    def render_self(self):
        self.screen.blit(self.images[self.id], (self.x, self.y))