import pygame as py
from animation import Animations
from database_management import JsonManagement as JM

class Introduction(Animations):
    def __init__(self, player, screen):
        super().__init__(player, screen)
        self.player = player
        self.introduction = not JM.get_specific_information('["player"]["animations_finished"]["introduction"]')


    def change_animation_state(self):
        animation_status = JM.open_file("saves")
        animation_status["player"]["animations_finished"]["introduction"] = True
        JM.write_file("saves", animation_status)

    def run(self):
        if not self.screen_animation_finished:
            self.player.direction = 2
            self.screen_animation(self.screen)
        else:
            if not self.dialog_finished:
                self.player.moving = False
                self.render_text_box(["Me voila enfin dans cette ville.", "Je dois trouver la bibliothèque.", "elle doit être dans cette direction."])
            elif self.dialog_finished:
                self.change_animation_state()
                self.introduction = False