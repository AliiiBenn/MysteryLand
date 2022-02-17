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
    def __init__(self):
        self.boutons = []
    
    def creer(self, screen, color):
        screen.fill(color)
        for index, bouton in enumerate(['play', 'option', 'exit']):
            bouton = Button (screen.get_width() / 2, screen.get_height() / 2 + ((index - 1) * 150), 180, 88, f'{bouton}_button')
            self.boutons.append(bouton)
            bouton.creer(screen)
            
    def check_state(self, state):
        for bouton in self.boutons:
            if bouton.check_collisions() and bouton.name == f'{state}_button':
                return True
            
    