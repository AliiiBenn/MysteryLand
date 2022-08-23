import sys, subprocess, pkg_resources

# required = {"pygame", "pyscroll", "pytmx", "firebase_admin", "requests", "pygame_widgets", "dataclasses"}
# installed = {pkg.key for pkg in pkg_resources.working_set}
# missing = required - installed

# if missing:
#     python = sys.executable
#     subprocess.check_call([python, "-m", "pip", "install", *missing], stdout=subprocess.DEVNULL)

import pygame as py
from game import Game


# on lance le jeu à partir d'ici
if __name__ == '__main__':
    py.init()
    py.font.init()
    game = Game(1200, 600)
    game.run()
