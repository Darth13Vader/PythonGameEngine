import pygame, threading
from PythonGameEngine.GameClasses.Block import Block
from PythonGameEngine.EngineClasses.Exceptions import *
from PythonGameEngine.EngineClasses.World import World
from PythonGameEngine.EngineClasses.Camera import Camera
from PythonGameEngine.EngineClasses.TextRenderer import TextRenderer
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

        self.world = World()
        self.sprites = {}

        self.camera.look_at_block(0, self.world.get_level_height() + 5)

    def set_up(self, *args, **kwargs):
        pass

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
                self.text_renderer.render_all()
            elif event.type == pygame.MOUSEBUTTONDOWN:
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

    def update_all(self, events):
        self.events_handler(events)
        #all_sprites = pygame.sprite.Group()
        self.screen.fill((140, 195, 218))
        for obj in self.world.get_level():
            x, y = self.transform_block_pos(obj.get_pos())
            self.screen.blit(self.sprites[obj.get_id()], (x, y))

        if self.selected_coords:
            x, y = self.transform_block_pos(self.selected_coords)
            self.screen.blit(self.sprites['selected'], (x, y))

        self.text_renderer.render_all()

        pygame.display.update()


if __name__ == '__main__':
    engine = PyGameEngine(1280, 720, resizable=True)
    engine.world.load_level('EngineClasses/level_1.txt')

    sprite_to_id = {'Sprites/grass.png': 'grass',
                    'Sprites/ground_1.png': 'ground',
                    'Sprites/selected_block_borders.png': 'selected'}

    engine.load_sprites(sprite_to_id)


    running = True
    fps = 60
    clock = pygame.time.Clock()

    keypressed_create_block = False
    keypressed_destroy_block = False

    cam_coeff = 15

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == MOUSE_CLICK_LEFT:
                    keypressed_create_block = True
                    x, y = engine.transform_screen_pos(event.pos)
                    res = engine.world.create_block(x, y, 'ground')
                    if res:
                        engine.text_renderer.add('res', 'Block created', -10, 10, alive_sec=1)
                elif event.button == MOUSE_CLICK_RIGHT:
                    keypressed_destroy_block = True
                    x, y = engine.transform_screen_pos(event.pos)
                    res = engine.world.destroy_block(x, y)
                    if res:
                        engine.text_renderer.add('res', 'Block destroyed', -10, 10, alive_sec=1)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == MOUSE_CLICK_LEFT:
                    keypressed_create_block = False
                elif event.button == MOUSE_CLICK_RIGHT:
                    keypressed_destroy_block = False
            elif event.type == pygame.MOUSEMOTION:
                if keypressed_create_block:
                    x, y = engine.transform_screen_pos(event.pos)
                    res = engine.world.create_block(x, y, 'ground')
                    if res:
                        engine.text_renderer.add('res', 'Block created', -10, 10, alive_sec=1)
                elif keypressed_destroy_block:
                    x, y = engine.transform_screen_pos(event.pos)
                    res = engine.world.destroy_block(x, y)
                    if res:
                        engine.text_renderer.add('res', 'Block destroyed', -10, 10, alive_sec=1)

        engine.camera.update(events)
        engine.update_all(events)
        clock.tick(fps)
