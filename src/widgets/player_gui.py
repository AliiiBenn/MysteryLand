import pygame as py

class PlayerGui:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.fulllife_heart = self.load_image("fulllife_heart", 45, 45)
        self.nolife_heart = self.load_image("nolife_heart", 45, 45)
        
    def load_image(self, image, width=None, height=None):
        image = py.image.load(f"img/{image}.png")
        if width and height:
            image = py.transform.scale(image, (width, height))
        image.set_colorkey([255, 0, 0])
        return image
        
    def display_life(self):
        for i in range(4):
            self.screen.blit(self.nolife_heart, (i * 50, 10))
        for i in range(int(self.player.life // 25)):
            self.screen.blit(self.fulllife_heart, (i * 50, 10))
        
    def display_quest_menu(self):
        quest_menu = self.load_image("quest_menu", 700, 500)
        rect = quest_menu.get_rect()
        rect.center = (self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.screen.blit(quest_menu, rect)