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

TILES_PATH = 'Sprites/Tiles/'

sprite_to_id = {TILES_PATH + 'grass.png': 'grass',
                TILES_PATH + 'grassCenter.png': 'grassCenter',
                TILES_PATH + 'grassLeft.png': 'grassLeft',
                TILES_PATH + 'grassMid.png': 'grassMid',
                TILES_PATH + 'grassRight.png': 'grassRight',
                TILES_PATH + 'stone.png': 'stone',
                TILES_PATH + 'stoneCenter.png': 'stoneCenter',
                TILES_PATH + 'stoneLeft.png': 'stoneLeft',
                TILES_PATH + 'stoneMid.png': 'stoneMid',
                TILES_PATH + 'stoneRight.png': 'stoneRight',
                TILES_PATH + 'castle.png': 'castle',
                TILES_PATH + 'castleCenter.png': 'castleCenter',
                TILES_PATH + 'castleLeft.png': 'castleLeft',
                TILES_PATH + 'castleMid.png': 'castleMid',
                TILES_PATH + 'castleRight.png': 'castleRight',
                'Sprites/background.png': 'background',
                'Sprites/myOwn/selected_block_borders.png': 'selected'}

# Family tag - tag
update_params = {'grass': {'0000': 'grass', '100x': 'grassRight', '010x': 'grassLeft', '110x': 'grassMid', 'other': 'grassCenter'},
                 'stone': {'0000': 'stone', '100x': 'stoneRight', '010x': 'stoneLeft', '110x': 'stoneMid', 'other': 'stoneCenter'},
                 'castle': {'0000': 'castle', '100x': 'castleRight', '010x': 'castleLeft', '110x': 'castleMid', 'other': 'castleCenter'}}
dec_dic = {'=': 'grass',
           '-': 'stone'}

engine.world.load_level('level_1.txt', dec_dic)
engine.world.set_update_params(update_params)
engine.world.update_all_level()
engine.camera.look_at_block(0, engine.world.get_level_height())

engine.load_sprites(sprite_to_id)
engine.world.set_update_params(update_params)
engine.setup(layouts_render=[('background', None),
                      ('world', engine),
                      ('entities', None),
                      ('Debug text', engine.text_renderer),
                      ('UI', engine.ui),
                      ('UI cover', None)])

image_to_id = {'Sprites/myOwn/ui_bottom_interface.png': 'interface_bottom_cell',
               'Sprites/myOwn/ui_bottom_interface_selected.png': 'interface_bottom_cell_selected'}
engine.ui.load_sprites(image_to_id)

bottom_ui = [Interface_button('interface_bottom_cell', 'center', -96*2, 'down', 5, 'grass', 'grass'),
             Interface_button('interface_bottom_cell', 'center', -96, 'down', 5, 'stone', 'stone'),
             Interface_button('interface_bottom_cell', 'center', 0, 'down', 5, 'castle', 'castle'),
             Interface_button('interface_bottom_cell', 'center', 96, 'down', 5),
             Interface_button('interface_bottom_cell', 'center', 96 * 2, 'down', 5)]

for unit in bottom_ui:
    unit.set_icons(engine.sprites)
    engine.ui.add(unit)

selected_ui = 0
bottom_ui[selected_ui].set_id('interface_bottom_cell_selected')

running = True
fps = 60
clock = pygame.time.Clock()

keypressed_create_block = False
keypressed_destroy_block = False

keys_down = {MOUSE_CLICK_LEFT: False,
             MOUSE_CLICK_MIDDLE: False,
             MOUSE_CLICK_RIGHT: False,
             MOUSE_SCROLL_UP: False,
             MOUSE_SCROLL_DOWN: False}
#keys_pressed = keys_down.copy()
keys_up = keys_down.copy()

mouse_pos = (0, 0)

cam_coeff = 15

while running:
    # ----- reset all keys -----
    for key, val in keys_down.items():
        keys_down[key] = False
        keys_up[key] = False
    # --------------------------
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            keys_down[event.button] = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = event.pos
            keys_up[event.button] = True
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos


    if keys_down[MOUSE_CLICK_LEFT]:
        keypressed_create_block = True
    if keys_down[MOUSE_CLICK_RIGHT]:
        keypressed_destroy_block = True
    if keys_down[MOUSE_SCROLL_UP]:
        bottom_ui[selected_ui].set_id('interface_bottom_cell')
        selected_ui -= 1
        if selected_ui == -1:
            selected_ui = 4
        bottom_ui[selected_ui].set_id('interface_bottom_cell_selected')
    if keys_down[MOUSE_SCROLL_DOWN]:
        bottom_ui[selected_ui].set_id('interface_bottom_cell')
        selected_ui += 1
        if selected_ui == 5:
            selected_ui = 0
        bottom_ui[selected_ui].set_id('interface_bottom_cell_selected')

    if keys_up[MOUSE_CLICK_LEFT]:
        keypressed_create_block = False
    if keys_up[MOUSE_CLICK_RIGHT]:
        keypressed_destroy_block = False

    if keypressed_create_block:
        x, y = engine.transform_screen_pos(mouse_pos)
        tag, family = bottom_ui[selected_ui].get_selected_block_info()
        #print(tag, family)
        if tag != '':
            cr_block = engine.world.create_block(x, y, tag, family)
            if cr_block:
                engine.text_renderer.add('res', 'Block created', -10, 10, alive_sec=1)
                nearest_blocks = engine.world.get_nearest_blocks(x, y)
                engine.world.update_block(*cr_block.get_pos())
                for nearest in nearest_blocks:
                    if nearest:
                        engine.world.update_block(*nearest.get_pos())
    elif keypressed_destroy_block:
        x, y = engine.transform_screen_pos(mouse_pos)
        res = engine.world.destroy_block(x, y)
        if res:
            engine.text_renderer.add('res', 'Block destroyed', -10, 10, alive_sec=1)
            nearest_blocks = engine.world.get_nearest_blocks(x, y)
            for nearest in nearest_blocks:
                if nearest:
                    engine.world.update_block(*nearest.get_pos())

    engine.text_renderer.add('fps', str(int(clock.get_fps())), -10, 10)
    engine.camera.update(events)
    engine.update_all(events)
    clock.tick(fps)