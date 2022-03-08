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
        """créer l'image sur l'écran

        Args:
            screen (_type_): écran
        """
        screen.blit(self.image, self.rect)
        
    def check_collisions(self) -> bool:
        """vérifie si l'on clique sur le bouton

        Returns:
            bool: true si collision
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

    def handle_event(self, event) -> bool:
        """evenement si on clique 

        Args:
            event (_type_): evenement

        Returns:
            bool: True 
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

    def update(self, x: int , y: int):
        """met a jour le screen

        Args:
            x (int): position en x
            y (int): position en y
        """
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width 
        self.rect.center = (x, y)

    def draw(self, screen):
        """dessine sur l'ecran

        Args:
            screen (_type_): écran
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
        if not in_game:
            self.screen.fill(color)
        for index, bouton in enumerate(['play', 'option', 'exit']):
            bouton = Button (self.screen.get_width() / 2, self.screen.get_height() / 2 + ((index - 1) * 150), 180, 88, f'{bouton}_button')
            self.boutons.append(bouton)
            bouton.creer(self.screen)
            
    def check_state(self, state):
        for bouton in self.boutons:
            if bouton.check_collisions() and bouton.name == f'{state}_button':
                return True
            
    def charger_menu_option(self):
        self.menu_option = py.image.load('img/option_menu.png')
        self.menu_option = py.transform.scale(self.menu_option, (self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.menu_option.set_colorkey([255 , 0, 0])
        self.menu_option_rect = self.menu_option.get_rect()
        self.menu_option_rect.center = (self.screen.get_width() / 2, self.screen.get_height() / 2)
        return self.menu_option_rect
    
    def mouse_collide_rect(self, tmx_data):
        mouse_pos = py.mouse.get_pos()
        for obj in tmx_data.objects:
            object_rect = py.Rect(obj.x * 2 + obj.width, obj.y * 2 + obj.height, obj.width, obj.height)
            if object_rect.collidepoint(mouse_pos):
                if py.mouse.get_pressed()[0]:
                    return True
                
            
    def creer_menu_options(self):
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
        self.screen.fill((0, 0, 255))
        self.user_input.update(self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.user_input.draw(self.screen)