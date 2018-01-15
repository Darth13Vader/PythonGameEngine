import pygame, time
from GameEngine import PyGameEngine

class TextRenderer:
    def __init__(self, engine: PyGameEngine):
        self.engine = engine
        self.all_labels = {}
        self.font = pygame.font.Font(None, 40)

    def add(self, id, text, x, y, alive_sec=None, color=(0, 0, 0)):
        rtext = self.font.render(text, 1, color)
        self.all_labels[id] = ([rtext, (x, y), [time.time(), alive_sec], id])

    def render_all(self):
        id_to_delete = []
        for text, pos, time_info, id in self.all_labels.values():
            if time_info[1]:
                if time.time() - time_info[0] > time_info[1]:
                    id_to_delete.append(id)
                    continue
            x, y = pos
            text_w, text_h = text.get_width(), text.get_height()
            scr_w, scr_h = self.engine.screen_w, self.engine.screen_h
            if pos[0] < 0:
                x = scr_w - text_w + x
            if pos[1] < 0:
                y = scr_h - text_h + y
            self.engine.screen.blit(text, (x, y))

        for id in id_to_delete:
            self.del_label(id)


    def get_labels(self):
        return self.all_labels

    def del_label(self, id):
        del self.all_labels[id]

    def reset(self):
        self.all_labels = {}