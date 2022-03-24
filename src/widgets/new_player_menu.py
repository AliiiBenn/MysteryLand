import pygame as py
from .input_box import InputBox


class NewPlayerMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = py.font.SysFont(None, 100)
        self.user_input = InputBox(self.screen.get_width() / 2, self.screen.get_height() / 2, 400, 100, "")
        
    def create(self):
        """Créé le menu de création de partie
        
        Args:
            La fonction ne prends aucun argument

        Returns :
            La fonction ne retourne rien --> None
        """
        self.screen.fill((0, 0, 255))
        self.user_input.update(self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.user_input.draw(self.screen)