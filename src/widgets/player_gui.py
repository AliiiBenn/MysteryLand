import pygame as py
from database_management import JsonManagement as JM

class PlayerGui:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.fulllife_heart = self.load_image("fulllife_heart", 45, 45)
        self.nolife_heart = self.load_image("nolife_heart", 45, 45)
        self.keys_text_count = 0
        self.keys_text_displayed = JM.get_specific_information('["player"]["keys_text_displayed"]')

        self.keys_text_list = ["Utilisez les touches z, q, s, d pour vous déplacer",
                               "Appuyez sur la touche f pour afficher le menu des quêtes",
                               "Appuyez sur la touche echap pour ouvrir le menu",
                               "Appuyez sur Espace pour parler aux NPC",
                               "En bas à droite il y a la distance vers la prochaine quête"]
        self.keys_text_list_index = 0
        
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

    def change_keys_text_status(self):
        data = JM.open_file("saves")
        data["player"]["keys_text_displayed"] = True
        JM.write_file("saves", data)


    def keys_help_text(self):
        self.keys_text_count += 1
        if self.keys_text_count % 100 == 0:
            self.keys_text_list_index += 1
        if self.keys_text_list_index >= len(self.keys_text_list) - 1 and self.keys_text_count >= (len(self.keys_text_list) * 100) - 1:
            self.keys_text_count = 0
            self.change_keys_text_status()
            self.keys_text_displayed = True

        text = self.keys_text_list[self.keys_text_list_index]
        font = py.font.SysFont("comicsansms", 25)
        label = font.render(text, 1, (0, 0, 0))
        self.screen.blit(label, (self.screen.get_width() // 2 - font.size(text)[0] // 2, self.screen.get_height() // 2))
        