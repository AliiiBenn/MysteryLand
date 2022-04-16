import pygame as py

class Son:
    def __init__(self):
        py.mixer.init()
        self.son = ""

    def finDuJeu(self):
        py.mixer.quit()


    def chercherSonCorrespondant(self):
        self.son = ""

class SonJoueur(Son):
    def __init__(self):
        pass

class SonPNJ(Son):
    def __init__(self, nomNpc):
        self.name = nomNpc

class SonGlobal(Son):
    def __init__(self):
        pass