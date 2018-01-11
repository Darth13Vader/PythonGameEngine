import pygame


class PGE_Button:
    def __init__(self, id, count_from_x, screen_x, count_from_y, screen_y, text=''):
        self.id = id
        self.count_from_x = count_from_x
        self.x = screen_x
        self.count_from_y = count_from_y
        self.y = screen_y
        self.text = ''

    def on_click_down(self):
        pass

    def on_click_up(self):
        pass

    def on_mouse_enter(self):
        pass

    def on_mouse_exit(self):
        pass

    def get_pos(self):
        return (self.count_from_x, self.x, self.count_from_y, self.y)