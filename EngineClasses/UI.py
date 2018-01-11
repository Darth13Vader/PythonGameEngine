import pygame


class UI:
    def __init__(self, screen):
        self.screen = screen
        self.interface = []

        self.images = {}

    def setup(self, *args, **kwargs):
        pass

    def add(self, id, x, y):
        if id not in self.images:
            return False
        pos_from_x, x, = x
        pos_from_y, y = y
        self.interface.append([id, pos_from_x, x, pos_from_y, y])

    def load_sprites(self, sprite_to_id):
        for filename, tag in sprite_to_id.items():
            sprite = pygame.image.load(filename).convert_alpha()
            self.images[tag] = sprite

    def render_all(self):
        for id, pos_from_x, x, pos_from_y, y in self.interface:
            if pos_from_x == 'center':
                x = self.screen.get_width() // 2 - self.images[id].get_width() // 2 + x
            elif pos_from_x == 'right':
                x = self.screen.get_width() - self.images[id].get_width() + x

            if pos_from_y == 'center':
                y = self.screen.get_height() // 2 + y
            elif pos_from_y == 'down':
                y = self.screen.get_height() - self.images[id].get_height() - y

            self.screen.blit(self.images[id], (x, y))