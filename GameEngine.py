import pygame, threading

class PyGameEngine:
    def __init__(self, screen_width, screen_height, resizable=False, title='PyGameEngine'):
        from GameClasses.Block import Block
        from EngineClasses.World import World
        from EngineClasses.Camera import Camera
        from EngineClasses.Input import Input
        from EngineClasses.TextRenderer import TextRenderer
        from EngineClasses.UI import UI
        pygame.init()

        if resizable:
            self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
        else:
            self.screen = pygame.display.set_mode((screen_width, screen_height))

        self.screen_w, self.screen_h = self.screen.get_width(), self.screen.get_height()

        pygame.display.set_caption(title)

        self.selected_coords = None
        self.block_height = 70

        self.camera = Camera(self)
        self.text_renderer = TextRenderer(self)
        self.ui = UI(self.screen)

        self.input = Input()

        self.world = World()
        self.sprites = {}

        self.layouts_renders = []
        self.layouts_rays = []

    def setup(self, *args, **kwargs):
        if 'layouts_render' in kwargs:
            self.layouts_renders = kwargs['layouts_render']
        if 'layouts_rays' in kwargs:
            self.layouts_rays = kwargs['layouts_rays']

    def load_sprites(self, sprite_to_id):
        for filename, tag in sprite_to_id.items():
            sprite = pygame.image.load(filename).convert_alpha()
            self.sprites[tag] = sprite

    def transform_screen_pos(self, screen_pos):
        screen_x, screen_y = screen_pos
        block_x = (screen_x - self.camera.get_position()[0] - 1) / self.block_height
        block_y = (self.camera.get_position()[1] - screen_y - 1) / self.block_height

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
        onscreen_x = block_x * self.block_height + self.camera.pos_x
        onscreen_y = - block_y * self.block_height + self.camera.pos_y
        return onscreen_x, onscreen_y

    def events_handler(self):
        if self.input.resizable:
            self.screen = pygame.display.set_mode(self.input.screen_size, pygame.RESIZABLE)
            self.screen_w, self.screen_h = self.screen.get_width(), self.screen.get_height()
            if 'background' in self.sprites:
                self.sprites['background'] = pygame.transform.scale(self.sprites['background'], (self.input.screen_size))
            self.text_renderer.render_all()

        selected_block = self.world.get_block(self.input.mousePos, self.camera.get_position())
        if selected_block:
            block_x, block_y = selected_block.pos_x, selected_block.pos_y
            self.selected_coords = (block_x, block_y)
            text = 'Block ({}, {})'.format(block_x, block_y)
            self.text_renderer.add('curr_block', text, 10, 10)
        else:
            self.selected_coords = None

    def render_all(self):
        self.events_handler()
        if 'background' in self.sprites:
            self.screen.blit(self.sprites['background'], (0, 0))
        else:
            self.screen.fill((140, 195, 218))
        for obj in self.world.get_level():
            x, y = self.transform_block_pos(obj.get_pos())
            if x < -self.block_height or y < -self.block_height or \
                    x > self.screen.get_width() + self.block_height or y > self.screen.get_height() + self.block_height:
                continue
            self.screen.blit(self.sprites[obj.get_tag()], (x, y))

        if self.selected_coords:
            x, y = self.transform_block_pos(self.selected_coords)
            self.screen.blit(self.sprites['selected'], (x, y))

    def update_all(self, events):
        self.input.get()
        for layout in self.layouts_renders:
            if layout[1]:
                layout[1].render_all()

        pygame.display.update()
