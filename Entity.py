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
        self.image = self.images[animation_name][self.animation_index]
        # self.image = py.transform.scale(self.image, (int(self.image.get_width() * self.scale), int(self.image.get_height() * self.scale)))
        self.image.set_colorkey([0, 0, 0])
        self.clock += self.speed * 8
        
        
        if self.clock >= 100:
            self.animation_index += 1
            
            if self.animation_index >= 6:
                self.animation_index = 0
            
            self.clock = 0
            
    def get_images(self, y : int, debut : int, fin : int) -> list:
        images = []
        
        for i in range(debut, fin):
            x = i*16
            image = self.get_image(x, y)
            images.append(image)
            
        return images
        
    def get_image(self, x, y):
        image = py.Surface([16, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 16, 32))
        return image


class Entity(Animation):
    def __init__(self, x, y, image_src):
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
        
    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        self.idling()
        
    def save_location(self):
        self.old_position = self.position.copy()
        
    def idling(self):
        direction = {0 : 'right', 1 : 'up', 2 : 'left', 3 : 'down'}
        if not self.moving:
            self.change_animation(f'idle_{direction[self.direction]}')
        
    def move_right(self):
        self.change_animation("walk_right")
        self.position[0] += self.speed
        self.moving, self.direction = True, 0
    
    def move_left(self):
        self.change_animation("walk_left")
        self.position[0] -= self.speed
        self.moving, self.direction = True, 2
    
    def move_up(self):
        self.change_animation("walk_up")
        self.position[1] -= self.speed
        self.moving, self.direction = True, 1
    
    def move_down(self):
        self.change_animation("walk_down")
        self.position[1] += self.speed
        self.moving, self.direction = True, 3

    # diagonales
    
    # def move_up_right(self):
    #     self.change_animation("walk_up")
    #     self.position[0] += self.speed/2
    #     self.position[1] -= self.speed/2
    #     self.moving, self.direction = True, 1
        
    # def move_up_left(self):
    #     self.change_animation("walk_up")
    #     self.position[0] -= self.speed/2
    #     self.position[1] -= self.speed/2
    #     self.moving, self.direction = True, 1

    # def move_down_left(self):
    #     self.change_animation("walk_down")
    #     self.position[0] -= self.speed/2
    #     self.position[1] += self.speed/2
    #     self.moving, self.direction = True, 3

    # def move_down_right(self):
    #     self.change_animation("walk_down")
    #     self.position[0] += self.speed/2
    #     self.position[1] += self.speed/2
    #     self.moving, self.direction = True, 3


    
    
    
    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        
    
