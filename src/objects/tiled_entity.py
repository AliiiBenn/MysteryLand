import pygame as py


class TiledEntity(py.sprite.Sprite):
    def __init__(self, x : int, y : int, sprite : str, width : int, height : int, tile_number : int, max_count : int):
        super().__init__()
        self.x = x
        self.y = y
        self.sprite = py.image.load(f'img/{sprite}.png')
        self.width = width
        self.height = height
        self.tile_number = tile_number
        self.max_count = max_count
        self.images = self.import_images()
        self.animation_index = 0
        self.clock = 0
        self.image = self.images[self.animation_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        
    def update(self):
        """Méthode principale de la class TiledEntity, elle est utilisée pour regrouper les méthodes utilisées
        """ 
        self.animate()
    
    def import_images(self, y : int = 0) -> list:
        """Méthode utilisée pour charger toutes les images de la TiledEntity, qui les enregistre dans une liste image_list

        Args:
            y (int, optional): ligne des images. Defaults to 0.

        Returns:
            list: retourne la liste une fois la boucle finie
        """
        images_list = []
        
        for position in range(self.tile_number):
            x = position * 16
            images_list.append(self.get_image(x, y))
            
        return images_list
            
        
    def get_image(self, x : int, y : int) -> None:
        """Méthode utilisée pour charger une image et la retourner

        Args:
            x (int): position de l'image en x 
            y (int): position de l'image en y

        Returns:
            _type_: retourne l'image
        """
        image = py.Surface([self.width, self.height])
        image.blit(self.sprite, (0, 0), (x, y, 16, 16))
        return image
    
    def animate(self):
        """Méthode principale d'animation de la TiledEntity avec un compteur 
        """
        self.clock += 1

        if self.clock >= self.max_count:
            self.clock = 0
            self.animation_index += 1
            
            if self.animation_index >= self.tile_number:
                self.animation_index = 0
            
            
            self.image = self.images[self.animation_index]
            self.image.set_colorkey([0, 0, 0])
            