from __future__ import annotations
from dataclasses import dataclass

from typing import Literal
import pygame as py 

class MovementVector2(py.math.Vector2):
    def __init__(self, x, y):
        super().__init__(x, y)
    
        
    @property
    def RIGHT(self) -> bool:
        return self.x >= 1
    
    @property
    def LEFT(self) -> bool:
        return self.x < 0
    
    @property
    def UP(self) -> bool:
        return self.y < 0
    
    @property
    def DOWN(self) -> bool:
        return self.y >= 1

class Input:
    def get_axis(direction : Literal["Horizontal", "Vertical"]) -> int:
        pressed = py.key.get_pressed()
        
        if direction == "Horizontal":
            left = pressed[py.K_q] or pressed[py.K_LEFT]
            right = pressed[py.K_d] or pressed[py.K_RIGHT]
            return right - left
        elif direction == "Vertical":
            up = pressed[py.K_z] or pressed[py.K_UP]
            down = pressed[py.K_s] or pressed[py.K_DOWN]
            return down - up
        
        return 0
    
    def get_vector() -> MovementVector2:
        return MovementVector2(
            Input.get_axis("Horizontal"),
            Input.get_axis("Vertical")
        )
            

class Animation(py.sprite.Sprite):
    def __init__(self, sprite : str):
        super().__init__()
        self.sprite_sheet = py.image.load(f"img/Entities/{sprite}_16x16.png")
        self.animation_index = 0
        self.clock = 0
        self.animation_speed = 2
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
            
        Returns :
            La fonction ne retourne rien --> None
        '''
        self.image = self.images[animation_name][self.animation_index]
        # self.image = py.transform.scale(self.image, (int(self.image.get_width() * self.scale), int(self.image.get_height() * self.scale)))
        
        self.image.set_colorkey([0, 0, 0])
        self.clock += self.animation_speed *  8
        
        
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
            x (int): position x de l'image
            y (int): position y de l'image

        Returns:
            sprite: une image
        """
        image = py.Surface([16, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 16, 32))
        return image


class Entity(Animation):
    def __init__(self, x : int, y : int, image_src):
        super().__init__(image_src)
        self.x : int = x
        self.y : int = y
        
        self.position : list[int] = [x, y]
        self.moving : bool = False
        self.direction : int = 0
        self.speed : float = 2.5
        
        self.image : py.Surface = py.Surface([16, 32])
        self.rect : py.Rect = self.image.get_rect()
        
        self.feet : py.Rect = py.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position : py.Rect = self.position.copy()
        
        
    def update(self) -> None:
        # self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        self.idling()
        
    def save_location(self) -> list[int]:
        self.old_position = self.position.copy()
        return self.old_position
        
    def check_entity_collision(self, entity : Entity) -> bool:
        return py.Rect.colliderect(self.rect, entity.rect)
        
    def idling(self) -> None:
        if not self.moving:
            directions = {0 : 'right', 1 : 'up', 2 : 'left', 3 : 'down'}
            self.change_animation(f'idle_{directions[self.direction]}')
            
    def animate(self, vector : MovementVector2) -> None:
        action = {
            vector.RIGHT : ('walk_right', 0),
            vector.LEFT: ('walk_left', 2),
            vector.DOWN : ('walk_down', 3),
            vector.UP : ('walk_up', 1)
        }
        print(vector.test())
        for key in action.keys():
            if key:
                self.direction = action[key][1]
                return self.change_animation(action[key][0])
                

    def move(self) -> None:
        new_direction = Input.get_vector()
        
        if new_direction.length_squared() > 0:
            self.animate(new_direction)
            new_direction.scale_to_length(self.speed)
            self.rect.move_ip(new_direction.x, new_direction.y)
           
            self.moving = True
            return
        self.moving = False


    def move_back(self) -> None:

        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom        
    
