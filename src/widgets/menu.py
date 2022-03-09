import pygame as py
import pytmx, pyscroll



class Button:
    def __init__(self, x, y, width, height, name):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.image = py.image.load(f'img/{name}.png')
        self.image = py.transform.scale(self.image, (self.width, self.height))
        self.image.set_colorkey([255 , 0, 0])
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.clicked = False
        
    def creer(self, screen) -> None:
        """Créer un nouveau bouton

        Args:
            screen (py.display): screen sur lequel on va afficher le bouton

        Returns :
            La fonction ne retourne rien --> None
        """
        screen.blit(self.image, self.rect)
        
    def check_collisions(self) -> bool:
        """Renvoie True si il y a collision entre un bouton et la souris
        
        Args:
            La fonction ne prends aucun argument

        Returns:
            bool: collision entre le bouton et la souris
        """
        mouse_pos = py.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if py.mouse.get_pressed()[0] and not self.clicked:
                return True
        
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.FONT = py.font.SysFont('Corbel', 75)
        self.color = (0, 0, 0)
        self.rect = py.Rect(x, y, w, h)
        self.rect.center = (x, y)
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event) -> list:
        """Méthode principale qui va gérer l'affichage du texte et la touche entrer

        Args:
            event (py.event): liste des evenements pygame

        Returns:
            list: renvoie une liste avec un booleen et le texte
        """
        if event.type == py.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
        if event.type == py.KEYDOWN:
            if self.active:
                if event.key == py.K_RETURN:
                    return [True, self.text]
                elif event.key == py.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.FONT.render(self.text, True, self.color)

    def update(self, x, y) -> None:
        """Met à jour l'input box

        Args:
            x (int): position en x
            y (int): position en y

        Returns :
            La fonction ne retourne rien --> None
        """
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width 
        self.rect.center = (x, y)

    def draw(self, screen):
        """Créer le bouton 

        Args:
            screen (py.display): l'ecran où l'input box va être affichée

        Returns :
            La fonction ne retourne rien --> None
        """
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        py.draw.rect(screen, self.color, self.rect, 2)    


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
            bouton = Button (self.screen.get_width() / 2, self.screen.get_height() / 2 + ((index - 1) * 150), 180, 88, f'{bouton}_button')
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
        
        
class NewPlayerMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = py.font.SysFont(None, 100)
        self.user_input = InputBox(self.screen.get_width() / 2, self.screen.get_height() / 2, 400, 100, "")
        
    def create(self):
        """Créé le menu de création de partie
        
        Args:
            La fonction ne prends aucun argument

        Returns :
            La fonction ne retourne rien --> None
        """
        self.screen.fill((0, 0, 255))
        self.user_input.update(self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.user_input.draw(self.screen)