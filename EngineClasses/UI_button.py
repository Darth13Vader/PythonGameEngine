import pygame


class PGE_Button:
    def __init__(self, id, count_from_x, screen_x, count_from_y, screen_y, text=''):
        self.id = id                        # self image id
        self.count_from_x = count_from_x    # Position on screen - right / center / left
        self.x = screen_x                   # Horizontal in pixels
        self.count_from_y = count_from_y    # Position on screen - up / center / down
        self.y = screen_y                   # Vertical in pixels
        self.text = ''                      # Button's text (can be replaced to anything else)

    def setup(self, screen, images):
        self.screen = screen                # Screen to render
        self.images = images                # All images dict to render

    def on_click_down(self):
        pass

    def on_click_up(self):
        pass

    def on_mouse_enter(self):
        pass

    def on_mouse_exit(self):
        pass

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_pos(self):
        return (self.count_from_x, self.x, self.count_from_y, self.y)

    def get_info(self):
        return self.id, self.count_from_x, self.x, self.count_from_y, self.y, self.text

    def update(self):
        self.render_self()
        self.render_other()

    def render_self(self):
        if self.count_from_x == 'center':
            x = self.screen.get_width() // 2 - self.images[self.id].get_width() // 2 + self.x
        elif self.count_from_x == 'right':
            x = self.screen.get_width() - self.images[self.id].get_width() + self.x
        elif self.count_from_x == 'left':
            x = self.x
        else:
            x = self.x

        if self.count_from_y == 'center':
            y = self.screen.get_height() // 2 + self.y
        elif self.count_from_y == 'down':
            y = self.screen.get_height() - self.images[self.id].get_height() - self.y
        elif self.count_from_y == 'up':
            y = self.y
        else:
            y = self.y

        self.screen.blit(self.images[self.id], (x, y))

    def render_other(self):
        pass

