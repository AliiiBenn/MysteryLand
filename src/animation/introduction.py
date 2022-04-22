import pygame as py
from animation import Animations

class Introduction(Animations):
    def __init__(self, player, screen):
        super().__init__(player, screen)
        self.player = player
        self.introduction = True
        self.movement = True

    def move_player_to_library(self):
        if not self.player.position[0] == 1056:
            self.player.left()
        else:
            if not self.player.position[1] == 2064:
                self.player.move_up()
            else:
                self.movement = False

    def run(self):
        if not self.screen_animation_finished:
            self.screen_animation(self.screen)
        else:
            self.move_player_to_library()
            if not self.dialog_finished and not self.movement:
                self.player.moving = False
                self.render_text_box(["Me voila enfin à la bibliothèque.", "Il faut que je trouve ce livre au plus vite.", "il est surement ici."])
            elif self.dialog_finished and not self.movement:
                self.introduction = False