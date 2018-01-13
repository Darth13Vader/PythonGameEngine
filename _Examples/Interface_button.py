from PythonGameEngine.EngineClasses.UI_button import PGE_Button

class Interface_button(PGE_Button):
    def __init__(self, id, count_from_x, screen_x, count_from_y, screen_y, tag='', family=''):
        super().__init__(id, count_from_x, screen_x, count_from_y, screen_y, text='')
        self.selected_block_tag = tag
        self.selected_block_family = family

    def set_icons(self, icons):
        self.icons = icons

    def get_selected_block_info(self):
        return self.selected_block_tag, self.selected_block_family

    def set_selected_block_info(self, tag, family):
        self.selected_block_tag = tag
        self.selected_block_family = family

    def render_other(self):
        if self.selected_block_tag != '':
            x, y = self.get_coordinates()
            ui_width, ui_height = self.images[self.id].get_width(), self.images[self.id].get_height()
            icon_width = self.icons[self.selected_block_tag].get_width()
            icon_height = self.icons[self.selected_block_tag].get_height()
            coords = (x + (ui_width - icon_width) // 2, y + (ui_height - icon_height) // 2)
            self.screen.blit(self.icons[self.selected_block_tag], coords)
