import pygame
from PythonGameEngine.EngineClasses.Exceptions import *


class Block(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, tag, family):
        super(Block, self).__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.tag = tag          # Block tag - ex. grassMid, grassLeft
        self.family = family    # Block family - ex. grass

        self.image = pygame.Surface((64, 64))
        self.rect = self.image.get_rect()

    def get_tag(self) -> int:
        return self.tag

    def set_tag(self, tag):
        self.tag = tag

    def get_family(self):
        return self.family

    def get_pos(self) -> tuple:
        return self.pos_x, self.pos_y