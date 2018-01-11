import pygame
from PythonGameEngine.EngineClasses.Exceptions import *


class Block(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, id):
        super(Block, self).__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.id = id

        self.image = pygame.Surface((64, 64))
        self.rect = self.image.get_rect()

    def get_id(self) -> int:
        return self.id

    def get_pos(self) -> tuple:
        return self.pos_x, self.pos_y