from PythonGameEngine.GameClasses.Block import Block


class LevelManager:
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
                    this_block = Block(xind - zero_x, zero_y, id, id)
                    blocks[(xind - zero_x, zero_y)] = this_block
                    # print('New Block: ({}, {})'.format(this_block.pos_x, this_block.pos_y))
            zero_y -= 1
        return blocks

    def save(self, blocks, decoder_dict, filename='recently.txt'):
        blocks_list = []
        for pos, block in blocks.items():
            blocks_list.append(((pos[0], pos[1]), block))
        blocks_list.sort(key=lambda x: (-x[0][1], x[0][0]))
        last_x, last_y = blocks_list[0][0][0], blocks_list[0][0][1]
        min_x = min(blocks_list, key=lambda x: x[0][0])[0][0]

        str_level = ''
        str_level += ' ' * (last_x - min_x)
        for pos, block in blocks_list:
            x, y = pos
            if y != last_y:
                str_level += '\n'
                str_level += ' ' * (x - min_x)
            if x - last_x > 1:
                str_level += ' ' * (x - last_x - 1)
            str_level += decoder_dict[block.get_family()]
            last_x, last_y = x, y

        with open(filename, 'w') as savefile:
            savefile.write(str_level)

