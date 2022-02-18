import pygame as py




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
            
    def creer_menu_options(self):
        self.charger_menu_option()
        self.screen.blit(self.menu_option, (self.menu_option_rect))
            
            
            
    