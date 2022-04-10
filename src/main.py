import pygame as py
from game import Game


# on lance le jeu à partir d'ici
if __name__ == '__main__':
    py.init()
    py.font.init()
    game = Game(1200, 600)
    game.run()

