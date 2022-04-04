import pygame as py
from pygame_widgets.textbox import TextBox


class NewPlayerMenu:
    def __init__(self, screen, menu):
        self.screen = screen
        self.menu = menu
        self.box = TextBox(self.screen, self.screen.get_width() / 2 - 400, self.screen.get_height() / 2 - 80, 800, 80, fontSize=50,
                borderColour=(255, 0, 0), textColour=(0, 200, 0),
                onSubmit=self.menu.create_new_player, radius=10, borderThickness=5)
        
    def create(self):
        return self.box