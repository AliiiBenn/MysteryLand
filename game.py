from xmlrpc.client import Boolean
import pygame as py
import requests
import player
from json_management import JsonManagement as JM
from map import MapManager
from menu import Menu, NewPlayerMenu

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
        
        self.playing = False
        self.open_menu = False
        self.option_open = False
        self.new_player_menu = NewPlayerMenu(self.screen)
        
                
        if not self.is_new_game():
            self.initialise_game()


    def update(self) -> None:
        self.map_manager.update()
        
    def initialise_game(self) -> None:
        '''
        inistialise le jeu
        '''
        self.open_menu = True    
        self.player = player.Player(0, 0, 100)
        self.map_manager = MapManager(self.screen, self.player)
        
    def is_new_game(self) -> bool:
        '''
        savoir si c'est la première connexion au jeu ou non
        '''
        return JM.get_specific_information('["player"]["new_game"]')
        
    def new_player(self, nickname: str) -> None:
        '''
        création d'un player avec notre id
        '''
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
        
    def change_game_status(self, state : int) -> None:
        '''
        change les données du joueur
        '''
        new_game = JM.open_file('saves')
        new_game["player"]["new_game"] = state
        JM.write_file('saves', new_game)
        
    def database_update_quitting(self) -> None:
        '''
        sauvegarde les données du joueur
        '''
        informations = self.player_informations.get_json_informations()
        self.player_informations.update_user_informations(
            informations["nickname"],
            informations["dungeons"],
            informations["money"],
            informations["level"][0],
            informations["level"][1]
        )
        
    def check_internet_connection(self) -> bool:
        '''
        test la connexion internet
        '''
        url = "http://www.google.com"
        timeout = 5
        try:
            request = requests.get(url, timeout=timeout)
            return True
        except (requests.ConnectionError, requests.Timeout) as exception:
            return False
        
    def ouvrir_menu(self) -> None:
        '''
        ouvre le menu
        '''
        menu = Menu(self.screen)
        if not self.playing:
            menu.creer((0, 0, 255))
            self.playing = menu.check_state('play')
            self.open_menu = not menu.check_state('play')
        else:
            menu.creer((0, 0, 255), True)
            self.open_menu = not menu.check_state('play')
    
    def handle_input(self) -> None:
        '''
        detection si une touche est pressée
        '''
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

    def run(self) -> None:
        '''
        lancer le jeu
        '''
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
            
            elif self.is_new_game():
                # print(JM.get_specific_information('["player"]["new_game"]'))
                # self.new_player('AliBen')
                # self.change_game_status(False)
                
                self.new_player_menu.create()
                    
            if self.open_menu:
                self.ouvrir_menu()
                
                
                    
            # else:
            #         menu = Menu(self.screen)
            #         menu.creer((0, 0, 255))
            #         self.playing = menu.check_state('play')
                
            # if self.open_menu:    
            #     if menu.check_state('exit'):
            #         running = False
            #         self.player.change_player_position()
            #         self.player.change_player_life(self.player.life)
            #         if self.check_internet_connection:
            #             self.database_update_quitting()
                    
            #     if menu.check_state('option'):
            #         self.option_open = True
                    
            #     if self.option_open:
            #         menu.creer_menu_options()
                
            #     if menu.quit_option:
            #         self.option_open = False   
            
            self.handle_input()
            py.display.flip()
            for event in py.event.get():
                if event.type == py.QUIT:
                    if self.playing:
                        self.player.change_player_position()
                        self.player.change_player_life(self.player.life)
                        if self.check_internet_connection:
                            self.database_update_quitting()
                    running = False
                elif event.type == py.VIDEORESIZE:
                    self.screen = py.display.set_mode(event.size, py.RESIZABLE)
                    if self.playing:
                        self.map_manager.change_zoom(event.size[0], event.size[1])
                if self.is_new_game():
                    enter_key_pressed = self.new_player_menu.user_input.handle_event(event)
                    if enter_key_pressed:
                        self.new_player(str(enter_key_pressed[1]))
                        self.change_game_status(False)
                        self.initialise_game()

            

        py.quit()