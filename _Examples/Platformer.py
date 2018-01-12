import pygame
import pygame, threading
from PythonGameEngine.GameEngine import PyGameEngine
from PythonGameEngine.GameClasses.Block import Block
from PythonGameEngine.EngineClasses.Exceptions import *
from PythonGameEngine.EngineClasses.World import World
from PythonGameEngine.EngineClasses.Camera import Camera
from PythonGameEngine.EngineClasses.TextRenderer import TextRenderer
from PythonGameEngine.EngineClasses.UI import UI
from PythonGameEngine.GlobalVariables.Keys import *
from PythonGameEngine.GlobalVariables.Constants import *

from Interface_button import Interface_button

engine = PyGameEngine(1280, 720, resizable=True)
engine.world.load_level('level_1.txt')
engine.camera.look_at_block(0, engine.world.get_level_height())

sprite_to_id = {'Sprites/grass.png': 'grass',
                'Sprites/ground_1.png': 'ground',
                'Sprites/selected_block_borders.png': 'selected'}

engine.load_sprites(sprite_to_id)
engine.setup(layouts_render=[('background', None),
                      ('world', engine),
                      ('entities', None),
                      ('Debug text', engine.text_renderer),
                      ('UI', engine.ui),
                      ('UI cover', None)])

image_to_id = {'Sprites/ui_bottom_interface.png': 'interface_bottom_cell',
               'Sprites/ui_bottom_interface_selected.png': 'interface_bottom_cell_selected'}
engine.ui.load_sprites(image_to_id)

bottom_ui = [Interface_button('interface_bottom_cell', 'center', -96*2, 'down', 5),
             Interface_button('interface_bottom_cell', 'center', -96, 'down', 5),
             Interface_button('interface_bottom_cell', 'center', 0, 'down', 5),
             Interface_button('interface_bottom_cell', 'center', 96, 'down', 5),
             Interface_button('interface_bottom_cell', 'center', 96 * 2, 'down', 5)]

for unit in bottom_ui:
    engine.ui.add(unit)

selected_ui = 0
bottom_ui[selected_ui].set_id('interface_bottom_cell_selected')

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
            elif event.button == MOUSE_SCROLL_UP:
                bottom_ui[selected_ui].set_id('interface_bottom_cell')
                selected_ui -= 1
                if selected_ui == -1:
                    selected_ui = 4
                bottom_ui[selected_ui].set_id('interface_bottom_cell_selected')
            elif event.button == MOUSE_SCROLL_DOWN:
                bottom_ui[selected_ui].set_id('interface_bottom_cell')
                selected_ui += 1
                if selected_ui == 5:
                    selected_ui = 0
                bottom_ui[selected_ui].set_id('interface_bottom_cell_selected')
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