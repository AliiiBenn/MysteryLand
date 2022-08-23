import pygame as py
import requests
import pygame_widgets
from entities.enemies import Enemies
from entities.player import Player, PlayerInformation, NewPlayer
from database_management.json_management import JsonManagement as JM
from maps import MapManager
from widgets import Menu, NewPlayerMenu, PlayerGui, DialogBox
from maps import Checkpoints
from objects import QuestsSystem, PositionQuests
from animation import Introduction, VolLivreAnimation, KidnappingAnimation

CLOCK = py.time.Clock()
FPS = 60

class Game:
    def __init__(self, screen_width: int, screen_height: int):
        self._screen_width = screen_width
        self._screen_height = screen_height
        self.screen = self.create_screen()
        
        self.player_informations = PlayerInformation()
        self.new_player_menu = NewPlayerMenu(self.screen, self)
        
        self.menu = Menu(self.screen)
        self.dialog_box = DialogBox()
        self.end_game_box_size = 0
        self.end_game_text = [
            "A suivre...",
            "Vous avez fini MysteryLand !",
            "Ce projet a été réalisé par David, Yanis et Jules",
            "Pour le projet de fin d'année de Terminale 2022",
            "En esperant que vous avez aimé le jeu !"
        ]
        
        
        
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
        self.quests_system = QuestsSystem(self.screen)
        self.map_manager = MapManager(self.screen, self.player, self.ennemy)
        self.introduction = Introduction(self.player, self.screen)
        self.vol_livre_animation = VolLivreAnimation(self.screen, self.player, self.map_manager)
        self.kidnapping_animation = KidnappingAnimation(self.player, self.map_manager, self.screen)
        if not JM.get_specific_information('["player"]["animations_finished"]["introduction"]'):
            self.introduction.teleport_player([1712, 2128])
        
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
            self.player.change_player_position(self.map_manager.current_map)
            self.player.change_player_life(self.player.life)
            if self.check_internet_connection:
                self.database_update_quitting()
            
    def end_game(self):
        py.draw.rect(self.screen, (0, 0, 0), (0, 0, self.screen.get_width(), self.end_game_box_size))
        if not self.end_game_box_size >= self.screen.get_height():
            self.end_game_box_size += 2.5
        else:
            for index, text in enumerate(self.end_game_text):
                font = py.font.SysFont("comicsansms", 25)
                label = font.render(text, 1, (255, 255, 255))
                self.screen.blit(label, (self.screen.get_width() // 2 - font.size(text)[0] // 2, (self.screen.get_height() // 2 + index * 50) - 200))
       
        
                
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
        
        if self.playing and not self.introduction.introduction:
            if pressed[py.K_e]:
                self.player.life -= 10
            elif pressed[py.K_ESCAPE]:
                if self.open_quest_menu:
                    self.open_quest_menu = False
                else:
                    self.open_menu = True

    def run(self) -> None:
        """Méthode principale qui lance le jeu

        Args:
            La fonction ne prends aucun argument
        
        Retruns :
            La fonction ne retourne rien -> None

        """
        running = True
        # library_pos_quest = PositionQuests(self.screen, 1063, 2077)
        positions_quest_list = [PositionQuests(self.screen, 1063, 2077, "World_Alpha", "Aller devant la bibliotheque", 10, 
                                PositionQuests(self.screen, 653, 435, "library", "Rentrer dans la bibliotheque", 10, 
                                PositionQuests(self.screen, 768, 192, "library", "Prendre le livre", 10,
                                PositionQuests(self.screen, 2571, 2884, "World_Alpha", "Recuperer votre livre", 10))))]
        start_thief_animation = False
        start_kidnapping_animation = False
        while running:
            CLOCK.tick(FPS)
            
            
            
            if self.playing:
                
                self.player.move()
                # print(self.player.moving)
                
                self.player.save_location()
                self.handle_input()
                self.update()
                self.map_manager.draw()
                self.dialog_box.render(self.screen)
                self.ennemy.is_entity_visible(self.player)

                current_map = self.map_manager.get_map()
                checkpoints = Checkpoints.get_checkpoints(current_map.tmx_data)


                if self.introduction.introduction:
                    self.introduction.run()
                else:
                    if not self.player_gui.keys_text_displayed:
                        self.player_gui.keys_help_text()
            
                for pos_quest in positions_quest_list:
                    if pos_quest.description == "Prendre le livre" and pos_quest.complete:
                        start_thief_animation = True
                    elif pos_quest.description == "Recuperer votre livre" and pos_quest.complete:
                        start_kidnapping_animation = True
                    if not pos_quest.complete:
                        self.quests_system._add_quest_to_dict(pos_quest)
                        pos_quest.update(self.map_manager.current_map, self.player)
                        self.quests_system.create_distance_text(self.player, pos_quest, self.screen.get_width() - 45, self.screen.get_height() - 40)
                    else:
                        self.quests_system.remove_quest(pos_quest, json_export=True)
                        if not pos_quest.complete_text_alpha <= 0:
                            self.quests_system.display_quest_text("Quête accomplie !", pos_quest)
                        else:
                            if pos_quest.has_next_quest:
                                positions_quest_list.append(pos_quest.next_quest)
                                positions_quest_list.remove(pos_quest)
                            else:
                                positions_quest_list.remove(pos_quest)
                        
                # print(positions_quest_list)
                        
                
                
                    
                self.player_gui.display_life()
                if self.open_quest_menu:
                    self.player_gui.display_quest_menu()
                    self.quests_system.display_quest_list(self.screen.get_width() / 2 - 300, self.screen.get_height() / 3)
                    

                if self.player.is_dead():
                    Checkpoints.teleport_to_checkpoints(self.player, checkpoints)
                    self.player.life = 100

                if not self.vol_livre_animation.animation_complete and start_thief_animation:
                    self.vol_livre_animation.create_screen_border(self.screen.get_width(), self.screen.get_height())
                    self.vol_livre_animation.move_thief(self.map_manager.voleur_library)

                if not self.kidnapping_animation.animation_complete and start_kidnapping_animation:
                    self.kidnapping_animation.run()

                if self.kidnapping_animation.animation_complete:
                    self.end_game()

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

                elif event.type == py.KEYDOWN:
                    if event.key == py.K_SPACE:
                        if self.playing:
                            self.map_manager.check_npc_collisions(self.dialog_box)
                    elif event.key == py.K_f and not self.introduction.introduction:
                        self.open_quest_menu = not self.open_quest_menu
                
                        
        py.quit()