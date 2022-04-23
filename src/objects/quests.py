import math
import pygame as py
from database_management import JsonManagement as JM

class QuestsSystem:
    def __init__(self, screen):
        self.screen = screen
        self.quests_dict = {}
        self.quests_list = []
        self.quest_text_x, self.quest_text_y = self.screen.get_width() // 2, self.screen.get_height() // 2
        
        
    def create_new_quests(self, description, position, xp, json_export=False):
        # Dans le cas où on veut stocker la quête dans le fichier json
        if json_export:
            path = JM.get_specific_information('["player"]["database_data"]["quests"]')
            if path == {} or not description in path:
                quests = JM.open_file("saves")
                quests["player"]["database_data"]["quests"][description] = {description:description, "position":position, "xp":xp}
                JM.write_file("saves", quests)
        # On regarde si la quête est déjà dans le json
        for quest in self.quests_dict:
            if description in quest or quest in description:
                return
        
        
    def display_quest(self, description, x, y):
        font = py.font.SysFont("comicsansms", 25)
        label = font.render(description, 1, (255, 255, 255))
        self.quests_list.append(label)
        return self.screen.blit(label, (x, y))

    def display_quest_list(self, x, y):
        for quest in self.quests_dict:
            self.display_quest(quest, x, y)
            y += 30

    def _add_quest_to_dict(self, quest):
        self.quests_dict[quest.description] = {"description":quest.description, "position":quest.position, "xp":quest.xp}

    def remove_quest(self, quest, json_export=False):
        if json_export:
            data = JM.open_file("saves")
            path = data["player"]["database_data"]["quests"]
            if quest.description in path:
                path.pop(quest.description)
                JM.write_file("saves", data)
        if quest.description in self.quests_dict:
            del self.quests_dict[quest.description]

    def distance_from_quest(self, player, quest, meters = True):
        if meters:
            return int(abs(player.rect.x - quest.x) / 32 + abs(player.rect.y - quest.y) / 32)
        return abs(player.rect.x - quest.x) + abs(player.rect.y - quest.y)

    def create_distance_text(self, player, quest, x, y):
        distance = self.distance_from_quest(player, quest)
        font = py.font.SysFont("comicsansms", 25)
        label = font.render(f"{distance}m", 1, (255, 255, 255))
        self.quests_list.append(label)
        return self.screen.blit(label, (x, y))

    def display_quest_text(self, text, quest):
        quest.complete_text_alpha -= 2
        font = py.font.SysFont("comicsansms", 25)
        render_text_list = [text, quest.description]
        for index, text in enumerate(render_text_list):
            text_size = font.size(text)
            label = font.render(text, 1, (0, 0, 0))
            label.set_alpha(quest.complete_text_alpha)
            self.screen.blit(label, (self.screen.get_width() // 2 - text_size[0] // 2, self.screen.get_height() // 2 - (text_size[1] if index == 0 else 0)))


class PositionQuests(QuestsSystem):
    def __init__(self, screen, x, y, world, description, xp, next_quest=None):
        super().__init__(screen)
        self.x = x
        self.y = y
        self.position = [self.x, self.y]
        self.world = world
        self.description = description
        self.xp = xp
        self.next_quest = next_quest
        self.position_rect = self.create_position_rect()
        self.complete = False
        self.complete_text_alpha = 255

    @property
    def has_next_quest(self):
        return self.next_quest is not None

    def update(self, world, player) -> None:
        self.create_new_quests(self.description, (self.x, self.y), self.xp, json_export=True)
        self.position_rect = self.create_position_rect()
        if self.player_collide_with_position(world, player.rect):
            self.complete_quest()
            
    def player_collide_with_position(self, current_world, player_rect) -> bool:
        """Méthode utilisée pour la collision avec le joueur"""
        return self.position_rect.colliderect(player_rect) and current_world == self.world

    def create_position_rect(self) -> py.Rect:
        """Méthode utilisée pour la position de la quête pour une futur collision avec le joueur"""
        return py.Rect(self.x, self.y, 32, 32)

    def complete_quest(self):
        self.complete = True
        return self.complete