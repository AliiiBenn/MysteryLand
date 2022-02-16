import pygame as py
from game import Game
from pygame.locals import *

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = (RED, GREEN, BLUE)
color_index = 0

class Home:
    def __init__(self):
        screen_width, screen_height = 1200, 600
        self.screen = py.display.set_mode((screen_width, screen_height), py.RESIZABLE)
        py.display.set_caption("MysteryLand")

        icon = py.image.load('img/logo.png')
        py.display.set_icon(icon)
        
        background = py.image.load('img/background.png')
        py.display.set_caption('background') 
    
    
    def play(self):
        stop = False
 
        clickable_area = py.Rect((100, 100), (100, 100))
        rect_surf = py.Surface(clickable_area.size)
        rect_surf.fill(COLORS[color_index])
        
        while not stop:
            for event in py.event.get():
                if event.type == py.QUIT:
                    stop = True
                
                elif event.type == MOUSEBUTTONUP: # quand je relache le bouton
                    if event.button == 1: # 1= clique gauche
                        if clickable_area.collidepoint(event.pos):
                            color_index = (color_index + 1) % 3
                            rect_surf.fill(COLORS[color_index])
            
            self.screen.fill(0) # On efface tout l'écran
            self.screen.blit(rect_surf, clickable_area)
            py.display.flip()
        
        py.quit()