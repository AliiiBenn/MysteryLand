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
        
    def creer(self, screen) -> None:
        """Créer un nouveau bouton

        Args:
            screen (py.display): screen sur lequel on va afficher le bouton

        Returns :
            La fonction ne retourne rien --> None
        """
        screen.blit(self.image, self.rect)
        
    def check_collisions(self) -> bool:
        """Renvoie True si il y a collision entre un bouton et la souris
        
        Args:
            La fonction ne prends aucun argument

        Returns:
            bool: collision entre le bouton et la souris
        """
        mouse_pos = py.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if py.mouse.get_pressed()[0] and not self.clicked:
                return True
        
