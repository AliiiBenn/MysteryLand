import pygame as py
from .entity import Entity
import math, random

class Enemies(Entity):
    def __init__(self, x : int, y : int, sprite : str, attack : float, screen):
        super().__init__(x, y, sprite)
        self.attack = attack
        self.screen = screen
        self.vision = py.Rect(self.rect.x, self.rect.y, 200 , 200)
        self.vision.center = (self.position[0], self.position[1])
        self.ai_counter = 0
        self.ia_direction = 0
        
    def update_vision_rect(self):
        self.vision = py.Rect(self.rect.x, self.rect.y, 300, 300)
        self.vision.center = (self.position[0], self.position[1])
        
    def is_entity_visible(self, entity : Entity):
        self.update_vision_rect()
        if py.Rect.colliderect(entity.rect, self.vision):
            self.follow_entity(entity)
        else:
            self.ai()
            
    def damage_entity(self, entity):
        if self.check_entity_collision(entity):
            entity.life -= self.attack
            
    def animate_ennemy(self, old_position):
        if old_position[0] < self.position[0] and self.position[0] - old_position[0] > self.position[1] - old_position[1]:
            self.moving, self.direction = True, 0
            self.change_animation('walk_right')
        if old_position[0] > self.position[0] and self.position[0] - old_position[0] < self.position[1] - old_position[1]:
            self.moving, self.direction = True, 2
            self.change_animation('walk_left')
        if old_position[1] < self.position[1] and self.position[1] - old_position[1] > self.position[0] - old_position[0]:
            self.moving, self.direction = True, 3
            self.change_animation('walk_down')
        if old_position[1] > self.position[1] and self.position[1] - old_position[1] < self.position[0] - old_position[0]:
            self.moving, self.direction = True, 1
            self.change_animation('walk_up')
        
    def follow_entity(self, entity : Entity) -> None:
        dx, dy = entity.position[0] - self.position[0], entity.position[1] - self.position[1]
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        old_position = [self.position[0], self.position[1]]
        self.position[0] += dx * (self.speed / 1.3)
        self.position[1] += dy * (self.speed / 1.3)
        self.animate_ennemy(old_position)
        
        
    def ai(self):
        if self.moving and random.randint(0, 500) == 250:
            self.moving = False
            self.idling()
            self.ai_counter = 0
        else:
            if self.moving:
                old_position = [self.position[0], self.position[1]]
                self.ai_counter += 1
                if self.ia_direction == 0:
                    self.position[0] += self.speed / 3
                if self.ia_direction == 1:
                    self.position[0] -= self.speed / 3
                if self.ia_direction == 2:
                    self.position[1] += self.speed / 3
                if self.ia_direction == 3:
                    self.position[1] -= self.speed / 3
                self.animate_ennemy(old_position)
            else:
                self.ai_counter += 1
                if self.ai_counter >= 100:
                    self.ia_direction = random.randint(0, 3)
                    self.moving = True
