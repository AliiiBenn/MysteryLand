import pygame as py
import player
from json_management import JsonManagement as JM
from map import MapManager
from menu import Menu

# test
CLOCK = py.time.Clock()
FPS = 60

class Game:
    def __init__(self):
        screen_width, screen_height = 1200, 600
        self.screen = py.display.set_mode((screen_width, screen_height), py.RESIZABLE)
        py.display.set_caption("MysteryLand")
        
        self.player_informations = player.PlayerInformation()

        icon = py.image.load('img/logo.png')
        py.display.set_icon(icon)
        if JM.get_specific_information('["player"]["new_game"]'):
            self.new_player('AliBen')
            self.not_new_game()
            
        self.player = player.Player(0, 0, 100)
        self.map_manager = MapManager(self.screen, self.player)
        
        self.playing = False
        self.open_menu = False
        self.option_open = False
        
        
    def update(self):
        self.map_manager.update()
        
    def new_player(self, nickname):
        player = JM.open_file('saves')
        
        player["player"].update({
            "position" : [0, 0],
            "life" : 100,
            "current_world" : "World",
            "database_data" : {
                "dungeons" : 0,
                "nickname" : nickname,
                "money" : 0,
                "level" : [0, 0]
            }
            
        })
        
        self.player_informations.update_user_informations(nickname, 0, 0, 0, 0)
        JM.write_file('saves', player)
        
    def not_new_game(self):
        new_game = JM.open_file('saves')
        new_game["player"]["new_game"] = False
        JM.write_file('saves', new_game)
        
    def database_update_quitting(self):
        informations = self.player_informations.get_json_informations()
        self.player_informations.update_user_informations(
            informations["nickname"],
            informations["dungeons"],
            informations["money"],
            informations["level"][0],
            informations["level"][1]
        )
    
    def handle_input(self):
        pressed = py.key.get_pressed()
        
        if self.playing:
            if pressed[py.K_z]:
                if pressed[py.K_q]:
                    self.player.move_left()
                elif pressed[py.K_d]:
                    self.player.move_right()
                self.player.move_up()
            elif pressed[py.K_s]:
                if pressed[py.K_q]:
                    self.player.move_left()
                elif pressed[py.K_d]:
                    self.player.move_right()
                self.player.move_down()
            elif pressed[py.K_q]:
                self.player.move_left()
            elif pressed[py.K_d]:
                self.player.move_right()
            elif pressed[py.K_e]:
                self.player.life -= 10
            elif pressed[py.K_ESCAPE]:
                self.open_menu = True
            else:
                self.player.moving = False
        if pressed[py.K_ESCAPE] and self.option_open:
            self.option_open = False

    def run(self):
        running = True
        while running:
            CLOCK.tick(FPS)
            
            
            
            if self.playing:
                self.player.save_location()
                self.update()
                self.map_manager.draw()
                
                if self.player.is_player_dead():
                    self.player.change_player_life(100)
                    running = False
                    
                if self.open_menu:
                    menu = Menu(self.screen)
                    menu.creer((0, 0, 255), True)
                    self.open_menu = not menu.check_state('play')
                    
                    
            else:
                menu = Menu(self.screen)
                menu.creer((0, 0, 255))
                self.playing = menu.check_state('play')
                
            if menu.check_state('exit'):
                running = False
                self.player.change_player_position()
                self.player.change_player_life(self.player.life)
                self.database_update_quitting()
                
            if menu.check_state('option'):
                self.option_open = True
                
            if self.option_open:
                menu.creer_menu_options()
            
            if menu.quit_option:
                self.option_open = False   
            
            self.handle_input()
            py.display.flip()
            for event in py.event.get():
                if event.type == py.QUIT:
                    if self.playing:
                        self.player.change_player_position()
                        self.player.change_player_life(self.player.life)
                        self.database_update_quitting()
                    running = False
                elif event.type == py.VIDEORESIZE:
                    self.screen = py.display.set_mode(event.size, py.RESIZABLE)
                    self.map_manager.change_zoom(event.size[0], event.size[1])

            

        py.quit()