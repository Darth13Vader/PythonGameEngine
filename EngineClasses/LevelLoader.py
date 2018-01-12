from PythonGameEngine.GameClasses.Block import Block


class LevelLoader:
    def __init__(self):
        pass

    def load(self, filename, decoder_dict):
        with open(filename) as datafile:
            level = [x.rstrip() for x in datafile.readlines()]

        zero_x = len(level[-1]) // 2
        zero_y = len(level) - 1

        blocks = {}
        for yind, row in enumerate(level):
            for xind, cell in enumerate(row):
                if cell in decoder_dict.keys():
                    id = decoder_dict[cell]
                    this_block = Block(xind - zero_x, zero_y, id)
                    blocks[(xind - zero_x, zero_y)] = this_block
                    #print('New Block: ({}, {})'.format(this_block.pos_x, this_block.pos_y))
            zero_y -= 1
        return blocks
