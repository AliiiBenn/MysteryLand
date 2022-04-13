import inspect
import pygame as py
import requests
import pygame_widgets
from entities.enemies import Enemies
from entities.player import Player, PlayerInformation, NewPlayer
from database_management.json_management import JsonManagement as JM
from maps import MapManager
from widgets import Menu, NewPlayerMenu, PlayerGui
from maps import Checkpoints
from objects import QuestsSystem

CLOCK = py.time.Clock()
FPS = 60

class NewGame:
    def __init__(self):
        pass

class Game:
    def __init__(self, screen_width: int, screen_height: int):
        self._screen_width = screen_width
        self._screen_height = screen_height
        self.screen = self.create_screen()
        
        self.player_informations = PlayerInformation()
        self.new_player_menu = NewPlayerMenu(self.screen, self)
        self.quests_system = QuestsSystem(self.screen)
        self.menu = Menu(self.screen)
        
        
        self.playing = False
        self.open_menu = True
        self.option_open = False
        self.open_quest_menu = False
        
        # if not self.is_new_game():
        #     self.initialise_game()
            
    @property
    def screen_width(self) -> int:
        return self._screen_width

    @property
    def screen_height(self) -> int:
        return self._screen_height
    
    def update(self) -> None:
        """Met à jour le système de map

        Args:
            La fonction ne prends aucun argument

        Returns :
            La fonction ne retourne rien --> None
        """
        self.map_manager.update()
    
    def create_screen(self) -> None:
        screen = py.display.set_mode((self._screen_width, self._screen_height), py.RESIZABLE)
        py.display.set_caption("MysteryLand")
        icon = py.image.load('img/logo.png')
        py.display.set_icon(icon)
        return screen

    def initialise_game(self) -> None:
        """Lance le jeu avec le menu, le joueur et la map
        
        Args:
            La fonction ne prends aucun argument

        Returns :
            La fonction ne retourne rien --> None
        """
        self.player = Player(0, 0, 100)
        self.player_gui = PlayerGui(self.screen, self.player)
        self.ennemy = Enemies(100, 100, 'Amelia', 0.3, self.screen)
        self.map_manager = MapManager(self.screen, self.player, self.ennemy)
        
    def is_new_game(self) -> bool:
        """Regarde si la partie est nouvelle

        Args:
            La fonction ne prends aucun argument

        Returns:
            bool: retourne un booleen qui correspond à l'etat de la partie, True si elle est nouvelle sinon False
        """
        return JM.get_specific_information('["player"]["new_game"]')
        
    def change_game_status(self, state : bool) -> None:
        """Change l'état du jeu quand une nouvelle partie est créee

        Args:
            state (bool): Etat du jeu qui correspond à state 

        Returns :
            La fonction ne retourne rien --> None
        """
        new_game = JM.open_file('saves')
        new_game["player"]["new_game"] = state
        JM.write_file('saves', new_game)
        
    def database_update_quitting(self) -> None:
        """Sauvegarde les données du joueur dans une base de donnée

        Args:
            La fonction ne prends aucun argument

        Returns :
            La fonction ne retourne rien --> None
        """
        informations = self.player_informations.get_json_informations()
        self.player_informations.update_user_informations(
            informations["nickname"],
            informations["dungeons"],
            informations["money"],
            informations["level"][0],
            informations["level"][1]
        )
        
    def check_internet_connection(self) -> bool:
        """Fais une requette internet pour savoir si l'ordinateur est connecté à internet

        Args
            La fonction ne prends aucun argument

        Returns:
            bool: renvoie l'état de la connexion, True si connecté sinon False
        """
        url = "http://www.google.com"
        timeout = 5
        try:
            request = requests.get(url, timeout=timeout)
            return True
        except (requests.ConnectionError, requests.Timeout) as exception:
            return False
        
    def ouvrir_menu(self) -> None:
        """Ouvre le menu

        Args:
            La fonction ne prends aucun argument

        Returns :
            La fonction ne retourne rien --> None
        """
        if not self.is_new_game():
            if not self.playing:
                self.menu.creer((0, 0, 255))
                if self.menu.check_state('play'):
                    
                    self.initialise_game()
                    self.playing = True
                self.open_menu = not self.menu.check_state('play')
            else:
                self.menu.creer((0, 0, 255), True)
                self.open_menu = not self.menu.check_state('play')
            
    def quit_game(self) -> None:
        """Méthode pour quitter le jeu et faire toutes les mises à jour nécéssaires

        Args:
            La fonction ne prends aucun argument

        Returns :
            La fonction ne retourne rien --> None
        """
        if self.playing:
            self.player.change_player_position()
            self.player.change_player_life(self.player.life)
            if self.check_internet_connection:
                self.database_update_quitting()
                
    def create_new_player(self):
        # on lance la fonction directement dans le widget
        if self.is_new_game():
            NewPlayer.create_new_player_informations(self.new_player_menu.box.getText(), self.player_informations)
            self.change_game_status(False)
            self.initialise_game()

            
    
    def handle_input(self) -> None:
        """Méthode qui gère toutes les entrées clavier du joueur

        Args:
            La fonction ne prends aucun argument

        Returns :
            La fonction ne retourne rien --> None
        
        """
        pressed = py.key.get_pressed()
        
        if self.playing:
            if pressed[py.K_z]:
                if pressed[py.K_q]:
                    self.player.move_left("u")
                elif pressed[py.K_d]:
                    self.player.move_right("u")
                else :
                    self.player.move_up()
            elif pressed[py.K_s]:
                if pressed[py.K_q]:
                    self.player.move_left("d")
                elif pressed[py.K_d]:
                    self.player.move_right("d")
                else :
                    self.player.move_down()
            elif pressed[py.K_q]:
                self.player.left()
            elif pressed[py.K_d]:
                self.player.right()
            elif pressed[py.K_e]:
                self.player.life -= 10
            elif pressed[py.K_f]:
                self.open_quest_menu = True
            elif pressed[py.K_ESCAPE]:
                if self.open_quest_menu:
                    self.open_quest_menu = False
                else:
                    self.open_menu = True
            else:
                self.player.moving = False

    def run(self) -> None:
        """Méthode principale qui lance le jeu

        Args:
            La fonction ne prends aucun argument
        
        Retruns :
            La fonction ne retourne rien -> None

        """
        running = True
        while running:
            CLOCK.tick(FPS)
            
            
            
            if self.playing:
                self.player.save_location()
                self.handle_input()
                self.update()
                self.map_manager.draw()
                self.ennemy.is_entity_visible(self.player)
                
                current_map = self.map_manager.get_map()
                checkpoints = Checkpoints.get_checkpoints(current_map.tmx_data)
                

                
                self.quests_system.create_new_quests("Tuer 30 monstres", (100, 100), 40, True)
                self.quests_system.create_new_quests("Aller au donjon", (100, 100), 40, True)
                    
                self.player_gui.display_life()
                if self.open_quest_menu:
                    self.player_gui.display_quest_menu()
                    for index, quest in enumerate(self.quests_system.quests_dict):
                        self.quests_system.display_quest(quest, self.screen.get_width() / 2 - 300, self.screen.get_height() / 3 + (index * 40))

                if self.player.is_dead():
                    Checkpoints.teleport_to_checkpoints(self.player, checkpoints)
                    self.player.life = 100
            
            elif self.is_new_game():
                self.new_player_menu.create()
                pygame_widgets.update(py.event.get())
                    
                    
            if self.open_menu:
                self.ouvrir_menu()
                if self.menu.check_state('exit'):
                    self.quit_game()
                    running = False
                
            
            py.display.flip()
            for event in py.event.get():
                
                if event.type == py.QUIT:
                    if self.playing:
                        self.quit_game()
                    running = False
                    
                elif event.type == py.VIDEORESIZE:
                    self.screen = py.display.set_mode(event.size, py.RESIZABLE)
                    if self.playing:
                        self.map_manager.change_zoom(event.size[0], event.size[1])
                        
        py.quit()