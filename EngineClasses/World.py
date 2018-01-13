from PythonGameEngine.GameClasses.Block import *
from PythonGameEngine.EngineClasses.LevelLoader import LevelLoader
from PythonGameEngine.GlobalVariables.Constants import *
from PythonGameEngine.GlobalVariables.Keys import *


class World:
    def __init__(self):
        self.blocks = {}
        self.update_params = {}

    def set_update_params(self, update_params):
        self.update_params = update_params

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

    def get_block_by_pos(self, block_pos) -> Block:
        x, y = block_pos
        if (x, y) in self.blocks:
            return self.blocks[(x, y)]

    def get_level(self):
        return self.blocks.values()

    def get_level_height(self):
        return sorted(self.blocks.keys(), key=lambda x: x[1], reverse=True)[0][1]

    def get_nearest_blocks(self, x, y) -> (Block, Block, Block, Block):
        if (x, y) not in self.blocks:
            return False

        if (x - 1, y) in self.blocks:
            bl_left = self.blocks[(x - 1, y)]
        else:
            bl_left = None

        if (x + 1, y) in self.blocks:
            bl_right = self.blocks[(x + 1, y)]
        else:
            bl_right = None
        if (x, y + 1) in self.blocks:
            bl_up = self.blocks[(x, y + 1)]
        else:
            bl_up = None
        if (x, y - 1) in self.blocks:
            bl_down = self.blocks[(x, y - 1)]
        else:
            bl_down = None

        return bl_left, bl_right, bl_up, bl_down

    def update_block(self, x, y):
        this_block = self.get_block_by_pos((x, y))
        if not this_block:
            return
        nearest = list(self.get_nearest_blocks(x, y))
        nearest_info = ''.join(['1' if block else '0' for block in nearest])
        this_family = this_block.get_family()
        if this_family in self.update_params:
            if nearest_info in self.update_params[this_family]:
                this_block.set_tag(self.update_params[this_family][nearest_info])
            else:
                for ind in range(4):
                    replaced_nearest = list(nearest_info)
                    replaced_nearest[ind] = 'x'
                    replaced_nearest = ''.join(replaced_nearest)
                    if replaced_nearest in self.update_params[this_family]:
                        this_block.set_tag(self.update_params[this_family][replaced_nearest])
                        return
                this_block.set_tag(self.update_params[this_family]['other'])

    def update_all_level(self):
        for x, y in self.blocks.keys():
            self.update_block(x, y)

    def create_block(self, x, y, id, family) -> Block:
        if self.get_block_by_pos((x, y)):
            return False
        bl = Block(x, y, id, family)
        self.blocks[(x, y)] = bl
        return bl

    def destroy_block(self, x, y):
        this_block = self.get_block_by_pos((x, y))
        if this_block:
            del self.blocks[(x, y)]
            return True
        return False
