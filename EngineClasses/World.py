from PythonGameEngine.GameClasses.Block import *
from PythonGameEngine.EngineClasses.LevelLoader import LevelLoader
from PythonGameEngine.GlobalVariables.Constants import *
from PythonGameEngine.GlobalVariables.Keys import *


class World:
    def __init__(self):
        self.blocks = {}

    def load_level(self, filename, dec_dic):
        try:
            level_loader = LevelLoader()
            self.blocks = level_loader.load(filename, dec_dic)
        except Exception as e:
            print('PGE.load_level ERROR:', e.args)

    def get_block(self, mouse_pos, camera_pos) -> Block:
        pos_x, pos_y = mouse_pos
        block_x = (pos_x - camera_pos[0] - 1) / BLOCK_HEIGHT
        block_y = (camera_pos[1] - pos_y - 1) / BLOCK_HEIGHT

        if block_x < 0:
            block_x = int(block_x) - 1
        else:
            block_x = int(block_x)

        if block_y > 0:
            block_y = int(block_y) + 1
        else:
            block_y = int(block_y)

        return self.get_block_by_pos((block_x, block_y))

    def get_block_by_pos(self, block_pos):
        x, y = block_pos
        if (x, y) in self.blocks:
            return self.blocks[(x, y)]

    def get_level(self):
        return self.blocks.values()

    def get_level_height(self):
        return sorted(self.blocks.keys(), key=lambda x: x[1], reverse=True)[0][1]

    def update_nearest_blocks(self, x, y):
        if (x, y) not in self.blocks:
            return False

        nearest_blocks = []

        if (x - 1, y) in self.blocks:
            bl_left = self.blocks[(x - 1, y)]
            nearest_blocks.append(bl_left)
        if (x + 1, y) in self.blocks:
            bl_right = self.blocks[(x + 1, y)]
            nearest_blocks.append(bl_right)
        if (x, y + 1) in self.blocks:
            bl_up = self.blocks[(x, y + 1)]
            nearest_blocks.append(bl_up)
        if (x, y - 1) in self.blocks:
            bl_down = self.blocks[(x, y - 1)]
            nearest_blocks.append(bl_down)

        return nearest_blocks

    def create_block(self, x, y, id):
        if self.get_block_by_pos((x, y)):
            return False
        bl = Block(x, y, id)
        self.blocks[(x, y)] = bl
        return True

    def destroy_block(self, x, y):
        this_block = self.get_block_by_pos((x, y))
        if this_block:
            del self.blocks[(x, y)]
            return True
        return False
