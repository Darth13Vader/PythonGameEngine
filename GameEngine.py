import pygame, threading
from PythonGameEngine.GameClasses.Block import Block
from PythonGameEngine.EngineClasses.Exceptions import *
from PythonGameEngine.EngineClasses.World import World
from PythonGameEngine.EngineClasses.Camera import Camera
from PythonGameEngine.EngineClasses.TextRenderer import TextRenderer
from PythonGameEngine.EngineClasses.UI import UI
from PythonGameEngine.GlobalVariables.Keys import *
from PythonGameEngine.GlobalVariables.Constants import *

class PyGameEngine:
    def __init__(self, screen_width, screen_height, resizable=False, title='PyGameEngine'):
        pygame.init()
        if resizable:
            self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
        else:
            self.screen = pygame.display.set_mode((screen_width, screen_height))

        pygame.display.set_caption(title)

        self.selected_coords = None

        self.camera = Camera(self.screen)
        self.text_renderer = TextRenderer(self.screen)
        self.ui = UI(self.screen)

        self.world = World()
        self.sprites = {}

        self.layouts_renders = []

    def setup(self, *args, **kwargs):
        if 'layouts_render' in kwargs:
            self.layouts_renders = kwargs['layouts_render']

    def load_sprites(self, sprite_to_id):
        for filename, tag in sprite_to_id.items():
            sprite = pygame.image.load(filename).convert_alpha()
            self.sprites[tag] = sprite
        # grass = pygame.image.load('Sprites/grass.png').convert()
        # ground_1 = pygame.image.load('Sprites/ground_1.png').convert()
        # selected_borders = pygame.image.load('Sprites/selected_block_borders.png').convert_alpha()

    def transform_screen_pos(self, screen_pos):
        screen_x, screen_y = screen_pos
        block_x = (screen_x - self.camera.get_position()[0] - 1) / BLOCK_HEIGHT
        block_y = (self.camera.get_position()[1] - screen_y - 1) / BLOCK_HEIGHT

        if block_x < 0:
            block_x = int(block_x) - 1
        else:
            block_x = int(block_x)

        if block_y > 0:
            block_y = int(block_y) + 1
        else:
            block_y = int(block_y)

        return block_x, block_y

    def transform_block_pos(self, block_pos):
        block_x, block_y = block_pos
        onscreen_x = block_x * BLOCK_HEIGHT + self.camera.pos_x
        onscreen_y = - block_y * BLOCK_HEIGHT + self.camera.pos_y
        return onscreen_x, onscreen_y

    def events_handler(self, events):
        for event in events:
            if event.type == pygame.RESIZABLE:
                self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                if 'background' in self.sprites:
                    self.sprites['background'] = pygame.transform.scale(self.sprites['background'], (event.size))
                self.text_renderer.render_all()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # self.camera.look_at_block(*self.transform_screen_pos(event.pos))
                # block = self.world.get_block(event.pos, self.camera.get_position())
                # if block:
                #     block_x, block_y = block.get_pos()
                #     scr_coords = self.transform_block_pos((block_x, block_y))
                #     bl_res = self.transform_screen_pos(scr_coords)
                #     print(scr_coords, event.pos, bl_res, block_x, block_y)
                pass

            elif event.type == pygame.MOUSEMOTION:
                selected_block = self.world.get_block(event.pos, self.camera.get_position())
                if selected_block:
                    block_x, block_y = selected_block.pos_x, selected_block.pos_y
                    self.selected_coords = (block_x, block_y)
                    text = 'Block ({}, {})'.format(block_x, block_y)
                    self.text_renderer.add('curr_block', text, 10, 10)
                else:
                    self.selected_coords = None

    def render_all(self):
        if 'background' in self.sprites:
            self.screen.blit(self.sprites['background'], (0, 0))
        else:
            self.screen.fill((140, 195, 218))
        for obj in self.world.get_level():
            x, y = self.transform_block_pos(obj.get_pos())
            self.screen.blit(self.sprites[obj.get_id()], (x, y))

        if self.selected_coords:
            x, y = self.transform_block_pos(self.selected_coords)
            self.screen.blit(self.sprites['selected'], (x, y))

    def update_all(self, events):
        self.events_handler(events)
        for layout in self.layouts_renders:
            if layout[1]:
                layout[1].render_all()

        pygame.display.update()
