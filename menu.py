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
        
    def creer(self, screen):
        screen.blit(self.image, self.rect)
        
    def check_collisions(self):
        mouse_pos = py.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if py.mouse.get_pressed()[0] and not self.clicked:
                return True
        
        


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
        
        # rendre un layer invisible
        # for layer in self.tmx_data.visible_layers:
        #     if layer.name == 'background':
        #         layer.visible = 0
        
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=5)
        
        # self.screen.fill((255, 0, 0))
        self.group.draw(self.screen)
        self.group.update()
        
        
        
        
        
        
        
        
        # print(tmx_data.visible_layers)
    