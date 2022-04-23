import pygame as py
from animation import Animations
from database_management import JsonManagement as JM


class VolLivreAnimation(Animations):
    def __init__(self, screen, player, map_manager):
        super().__init__(player, screen)
        self.screen = screen
        self.map_manager = map_manager
        self.player = player
        self.border_position = 0
        self.border_count = 0
        self.border_complete = False
        self.book_stolen = False
        self.animation_complete = JM.get_specific_information('["player"]["animations_finished"]["thief"]')

    def change_animation_state(self):
        animation_status = JM.open_file("saves")
        animation_status["player"]["animations_finished"]["thief"] = True
        JM.write_file("saves", animation_status)

    

    def move_thief(self, thief):
        if not self.book_stolen:
            if not thief.position[0] >= self.player.position[0]:
                thief.move_right()
            else:
                if not thief.position[1] <= self.player.position[1] + 16:
                    thief.move_up()
                else:
                    thief.moving = False
                    if self.render_text_box(["Que fais tu avec ce livre ?", "Il est à moi desormais !", "Essaye de me retrouver pour voir !!"]):
                        self.book_stolen = True
        else:
            if not thief.position[0] <= 543 and not thief.position[1] == 445:
                thief.move_left()
            else:
                if not thief.position[1] == 445:
                    thief.move_down()
                else:
                    if not thief.position[0] >= 630:
                        thief.move_right()
                    else:
                        thief.kill()
                        self.animation_complete = True
                        self.change_animation_state()