import pygame as py

musiques = []


class Son:
    def __init__(self, nomDuFichier):
        py.mixer.init()
        self.son = py.mixer.Sound(nomDuFichier)

    def finDuJeu(self):
        py.mixer.quit()

    def stopSon(self):
        pass

class SonJoueur(Son):
    def __init__(self):
        pass

class SonPNJ(Son):
    def __init__(self, nomNpc):
        self.name = nomNpc

class SonGlobal(Son):
    def __init__(self):
        pass