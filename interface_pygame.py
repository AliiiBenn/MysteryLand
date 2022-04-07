import pygame
import pygame.gfxdraw
import time
from math import pi, sin, cos

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

################################################################################
#
#   Module d'interface utilisateur (version pygame)
#
################################################################################
# bonne documentation pygame : https://realpython.com/pygame-a-primer/


class Interface_pygame:
    def __init__(self, jeu = None):
        self.jeu = jeu
        self.run = True
        pygame.init()
        pygame.display.set_caption('PacWoman')

        # Une horlaoge pour rythmer l'affichage
        self.horloge = pygame.time.Clock()
        self.fps = 2

        # Calcul des dimensions
        self.d = 100 # taille d'une case (en px)
        self.w = self.d*self.jeu.w
        self.h = self.d*self.jeu.h

        # Fenêtre de dessin
        self.screen = pygame.display.set_mode([self.w, self.h])


    def rafraichir(self):
        return


    def quitter(self):
        """ Quitte l'interface
        """
        # Ici faire ce qu'il faut avant de quitter ...
        self.__del__()

        
    def __del__(self):
        """ Méthode appelée automatiquement à la destruction de l'objet
        """
        pygame.quit()
    

    def lancer(self):
        while self.run:
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == QUIT:
                    # éventuellement mettre ici une condition (avec retour au jeu)
                    # pour demander confirmation à l'utilisateur par exemple
                    self.run = False

                # autres événements ....

            # Arrière plan uni (blanc)
            self.screen.fill((0, 0, 0))

            # Dessin ..........
            self.draw_pacman(0, 0)

            pygame.display.flip()
            self.horloge.tick(self.fps)
        self.quitter()


    def action_clavier(self, event):
        ''' Pour Pac '''
        if self.jeu is not None:
            self.jeu.action_clavier(event.name)
        else:
            print(event.name)
            
    def draw_pacman(self, l, c):
        """ Dessine un Pacman à la ligne l et la colonne c de la grille
        """
        self.fill_arc(int((c+0.5)*self.d), int((l+0.5)*self.d), self.d//3,
                      pi/8, 15*pi/8, (0xFF, 0xF2, 0x00))


    def fill_arc(self, x, y, radius, theta0, theta1, color):
        ndiv = 20
        d_theta = (theta1 - theta0) / ndiv

        x0 = int(x + radius * cos(theta0))
        y0 = int(y + radius * sin(theta0))

        for i in range(1, ndiv):
            x1 = int(x + radius * cos(theta0 + i*d_theta))
            y1 = int(y + radius * sin(theta0 + i*d_theta))
            pygame.gfxdraw.filled_trigon(self.screen, x, y, x0, y0, x1, y1, color)
            x0, y0 = x1, y1