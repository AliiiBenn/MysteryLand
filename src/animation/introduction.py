import pygame as py
from animation import Animations

class Introduction(Animations):
    def __init__(self, player, screen):
        super().__init__(player, screen)
        self.player = player
        self.introduction = True

    def move_player_to_library(self):
        if not self.player.position[0] == 1056:
            self.player.left()
        else:
            if not self.player.position[1] == 2064:
                self.player.move_up()
            else:
                self.introduction = False

    def run(self):
        if not self.screen_animation_finished:
            self.screen_animation(self.screen)
        else:
            self.move_player_to_library()