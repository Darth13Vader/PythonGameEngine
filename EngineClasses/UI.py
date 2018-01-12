import pygame
from PythonGameEngine.EngineClasses.UI_button import PGE_Button

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.interface = []

        self.images = {}

    def setup(self, *args, **kwargs):
        pass

    def add(self, interface_unit: PGE_Button):
        if interface_unit.get_id() not in self.images:
            return False
        interface_unit.setup(self.screen, self.images)
        self.interface.append(interface_unit)

    def load_sprites(self, sprite_to_id):
        for filename, tag in sprite_to_id.items():
            sprite = pygame.image.load(filename).convert_alpha()
            self.images[tag] = sprite

    def render_all(self):
        for interface_unit in self.interface:
            interface_unit.render()
