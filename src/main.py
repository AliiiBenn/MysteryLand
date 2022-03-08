import pygame as py
from game import Game


# on lance le jeu à partir d'ici
if __name__ == '__main__':
    py.init()
    game = Game()
    game.run()
