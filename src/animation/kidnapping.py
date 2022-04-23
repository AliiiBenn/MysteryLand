import pygame as py
from animation import Animations
from database_management import JsonManagement as JM

class KidnappingAnimation(Animations):
    def __init__(self, player, map_manager, screen):
        super().__init__(player, screen)
        self.screen = screen
        self.player = player
        self.map_manager = map_manager
        self.thief = self.map_manager.voleur_world
        self.animation_complete = JM.get_specific_information('["player"]["animations_finished"]["kidnapping"]')

    def run(self):
        self.create_screen_border(self.screen.get_width(), self.screen.get_height())
        self.move_thief(self.thief)

    def change_animation_state(self):
        animation_status = JM.open_file("saves")
        animation_status["player"]["animations_finished"]["kidnapping"] = True
        JM.write_file("saves", animation_status)

    def move_thief(self, thief):
        if not thief.position[0] >= self.player.position[0]:
            thief.move_right()
        else:
            if not thief.position[1] <= self.player.position[1] + 16:
                thief.move_up()
            else:
                self.thief.moving = False
                self.player.kill()
                self.animation_complete = True
                self.change_animation_state()