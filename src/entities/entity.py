import pygame as py 



class Animation(py.sprite.Sprite):
    def __init__(self, sprite : str):
        super().__init__()
        self.sprite_sheet = py.image.load(f"img/{sprite}_16x16.png")
        self.animation_index = 0
        self.clock = 0
        self.speed = 2
        self.images = {
            'idle_right' : self.get_images(32, 0, 6),
            'idle_up' : self.get_images(32, 6, 12),
            'idle_left' : self.get_images(32, 12, 18),
            'idle_down' : self.get_images(32, 18, 24),
            'walk_right' : self.get_images(64, 0, 6),
            'walk_up' : self.get_images(64, 6, 12),
            'walk_left' : self.get_images(64, 12, 18),
            'walk_down' : self.get_images(64, 18, 24)
        }
        
    def change_animation(self, animation_name : str) -> None:
        '''Charge l'image suivante de l'animation "animation_name".
        
        Args :
            animation_name (str) : nom de l'animation
            
        Returns : None
        '''
        self.image = self.images[animation_name][self.animation_index]
        # self.image = py.transform.scale(self.image, (int(self.image.get_width() * self.scale), int(self.image.get_height() * self.scale)))
        
        self.image.set_colorkey([0, 0, 0])
        self.clock += self.speed *  8
        
        
        if self.clock >= 100:
            self.animation_index += 1
            
            if self.animation_index >= 6:
                self.animation_index = 0
            
            self.clock = 0
            
    def get_images(self, y : int, debut : int, fin : int) -> list:
        """Obtient les images

        Args:
            y (int): ligne d'image
            debut (int): debut de la ligné d'image
            fin (int): fin de la ligné d'image

        Returns:
            list: liste des images
        """
        images = []
        
        for i in range(debut, fin):
            x = i*16
            image = self.get_image(x, y)
            images.append(image)
            
        return images
        
    def get_image(self, x : int, y : int):
        """Obtient une image

        Args:
            x (int): _description_
            y (int): _description_

        Return:
            sprite: une image
        """
        image = py.Surface([16, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 16, 32))
        return image


class Entity(Animation):
    def __init__(self, x : int, y : int, image_src):
        super().__init__(image_src)
        self.x = x
        self.y = y
        self.image = py.Surface([16, 32])
        # self.image = py.transform.scale(self.image, (int(self.image.get_width() * self.scale), int(self.image.get_height() * self.scale)))
        # self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = py.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        self.moving = False
        self.direction = 0
        
    def update(self) -> None:
        """Met à jour la page: update

        Return :
            None        
        """
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        self.idling()
        
    def save_location(self) -> None:
        """Sauvgarde la position

        Returns :
            None  
        """
        self.old_position = self.position.copy()
        
    def idling(self) -> None:
        """Détermine la direction dans laquelle avance le perosnnage pour l'animation

        Returns :
            None  
        """
        direction = {0 : 'right', 1 : 'up', 2 : 'left', 3 : 'down'}
        if not self.moving:
            self.change_animation(f'idle_{direction[self.direction]}')

    '''
    ------------------------------------------
    Directions + gestion de la diagonale :
    ------------------------------------------
    '''
    
    def move_up(self, diagonale = False) -> None:
        """Fonction qui permet le deplacement haut et diagonale haut (dans les deux directions)

        Args:
            param1: diagonale (False par défaut)

        Returns:
            La fonction ne retourne rien --> None
        """
        if diagonale :
            #self.change_animation("walk_up", True)
            self.position[1] -= self.speed #+ 0.45
        else :
            self.change_animation("walk_up")
            self.position[1] -= self.speed
        self.moving, self.direction = True, 1
    
    def move_down(self, diagonale = False) -> None:
        """Fonction qui permet le deplacement bas et diagonale bas (dans les deux directions)

        Args:
            param1: diagonale (False par défaut)

        Returns:
            La fonction ne retourne rien --> None
        """
        if diagonale :
            self.position[1] += self.speed
        else :
            self.change_animation("walk_down")
            self.position[1] += self.speed
        self.moving, self.direction = True, 3
        
    def right(self, diagonale = False): 
        """Fonction qui permet le deplacement à droite (plus ou moins vite si le joueur se déplace en diagonale)

        Args:
            param1: diagonale (False par défaut)

        Returns:
            La fonction ne retourne rien --> None
        """
        if diagonale : 
            self.change_animation("walk_right")
            self.position[0] += (self.speed//2)
        else : 
            self.change_animation("walk_right")
            self.position[0] += self.speed #Seulement droite
        self.moving, self.direction = True, 0

    def left(self, diagonale = False): 
        """Fonction qui permet le deplacement à gauche (plus ou moins vite si le joueur se déplace en diagonale)

        Args:
            param1: diagonale (False par défaut)

        Returns:
            La fonction ne retourne rien --> None
        """
        if diagonale : 
            self.change_animation("walk_left")
            self.position[0] -= (self.speed//2) 
        else : 
            self.change_animation("walk_left")
            self.position[0] -= self.speed #Seulement gauche
        self.moving, self.direction = True, 2

    def move_right(self, diagonale = '') -> None:
        """Fonction qui interprète l'argument fourni par la méthode Game.handle_input pour connaitre la direction du déplacement droit (diagonale ou pas ? --> Si oui, diagonale haut ou bas ?)
        'u' = up (droite + haut)
        'd' = down (droite + bas)
        '' = right (droite sans diagonale)

        Args:
            param1: diagonale ('' par défaut)

        Returns:
            La fonction ne retourne rien --> None
        """
        if diagonale == 'u' :
            self.move_up(True)
            self.right(True)
        elif diagonale == 'd' :
            self.move_down(True)
            self.right(True)
        else :
            self.right()
    
    def move_left(self, diagonale = '') -> None:
        """Fonction qui interprète l'argument fourni par la méthode Game.handle_input pour connaitre la direction du déplacement gauche (diagonale ou pas ? --> Si oui, diagonale haut ou bas ?)
        'u' = up (gauche + haut)
        'd' = down (gauche + bas)
        '' = left (gauche sans diagonale)

        Args:
            param1: diagonale ('' par défaut)

        Returns:
            La fonction ne retourne rien --> None
        """
        if diagonale == 'u' :
            self.move_up(True)
            self.left(True)
        elif diagonale == 'd' :
            self.move_down(True)
            self.left(True)
        else :
            self.left()

    def move_back(self) -> None:
        """Reviens a la position precedente apres avoir heurter un bloc de type collision

        Returns :
            None  
        """
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        
    
