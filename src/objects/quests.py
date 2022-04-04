import pygame as py
from database_management import JsonManagement as JM

class QuestsSystem:
    def __init__(self, screen):
        self.screen = screen
        self.quests_dict = {}
        self.quests_list = []
        
    def create_new_quests(self, description, position, xp, json_export=False):
        if json_export:
            path = JM.get_specific_information('["player"]["database_data"]["quests"]')
            if path == {} or not description in path:
                quests = JM.open_file("saves")
                quests["player"]["database_data"]["quests"][description] = {description:description, "position":position, "xp":xp}
                JM.write_file("saves", quests)
        for quest in self.quests_dict:
            if description in quest or quest in description:
                return
        self.quests_dict[description] = {description:description, "position":position, "xp":xp}
        
    def display_quest(self, description, x, y):
        font = py.font.SysFont("comicsansms", 25)
        label = font.render(description, 1, (255, 255, 255))
        self.quests_list.append(label)
        # print(label.get_rect())
        return self.screen.blit(label, (x, y))