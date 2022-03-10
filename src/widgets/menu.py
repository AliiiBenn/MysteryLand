import pygame as py
import pytmx, pyscroll
from .button import Button



class Menu:
    def __init__(self, screen):
        self.boutons = []
        self.screen = screen
        self.tmx_data = pytmx.util_pygame.load_pygame(f'Maps/menu_option.tmx')
        self.quit_option = self.mouse_collide_rect(self.tmx_data)
    
    def creer(self, color, in_game=False):
        """Méthode qui créée le menu

        Args:
            color (tuple): couleur du menu 
            in_game (bool, optional): Savoir si le joueur est en jeu. Defaults to False.

        Returns :
            La fonction ne retourne rien --> None
        """
        if not in_game:
            self.screen.fill(color)
        for index, bouton in enumerate(['play', 'option', 'exit']):
            bouton = Button(self.screen.get_width() / 2, self.screen.get_height() / 2 + ((index - 1) * 150), 180, 88, f'{bouton}_button')
            self.boutons.append(bouton)
            bouton.creer(self.screen)
            
    def check_state(self, state):
        """Vérifie si il y a une collision entre le bouton state et la souris

        Args:
            state (str): nom du bouton

        Returns:
            bool: True si il y a collision sinon False
        """
        for bouton in self.boutons:
            if bouton.check_collisions() and bouton.name == f'{state}_button':
                return True
            
    def charger_menu_option(self):
        """A faire

        Args :
            La fonction ne prends aucun argument

        Returns :
            
        """
        self.menu_option = py.image.load('img/option_menu.png')
        self.menu_option = py.transform.scale(self.menu_option, (self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.menu_option.set_colorkey([255 , 0, 0])
        self.menu_option_rect = self.menu_option.get_rect()
        self.menu_option_rect.center = (self.screen.get_width() / 2, self.screen.get_height() / 2)
        return self.menu_option_rect
    
    def mouse_collide_rect(self, tmx_data):
        """A faire

        Args :

        Returns :
        """

        mouse_pos = py.mouse.get_pos()
        for obj in tmx_data.objects:
            object_rect = py.Rect(obj.x * 2 + obj.width, obj.y * 2 + obj.height, obj.width, obj.height)
            if object_rect.collidepoint(mouse_pos):
                if py.mouse.get_pressed()[0]:
                    return True
                
            
    def creer_menu_options(self):
        """Créé le menu d'options
        
        Args:
            La fonction ne prends aucun argument

        Returns :
            La fonction ne retourne rien --> None
        """
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 2
        
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=5)
        self.group.draw(self.screen)
        self.group.update()
        
        
