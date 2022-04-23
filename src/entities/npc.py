import math
import pygame as py
from .entity import Entity


class NPC(Entity):
    def __init__(self, x : int, y : int, sprite : str) -> None:
        super().__init__(x, y, sprite)


class Specialnpc(NPC):
    def __init__(self, x : int, y : int, sprite : str) -> None:
        super().__init__(x, y, sprite)

class Voleur(NPC):
    def __init__(self, x : int, y : int, sprite : str) -> None:
        super().__init__(x, y, sprite)
        
# TODO : Régler le problème de collisions quand la speed est à 1 (déjà vu chez la conference woman).        
class Basicnpc(NPC):
    def __init__(self, sprite : str, nb_points : int, dialog_list : list[str]) -> None:
        super().__init__(0, 0, sprite)
        self.nb_points = nb_points
        self.dialog_list = dialog_list
        self.coordinates_list = []
        self.points = []
        self.speed = 1
        self.name = sprite
        self.current_point = 0
        self.path_direction = 1
        
    def animate_npc(self, old_position, npc_rect, target_rect):
        if old_position[0] < self.position[0] and abs(target_rect.x - npc_rect.x) > abs(target_rect.y - npc_rect.y):
            self.moving, self.direction = True, 0
            self.change_animation('walk_right')
        if old_position[0] > self.position[0] and abs(target_rect.x - npc_rect.x) > abs(target_rect.y - npc_rect.y):
            self.moving, self.direction = True, 2
            self.change_animation('walk_left')
        if old_position[1] < self.position[1] and abs(target_rect.x - npc_rect.x) < abs(target_rect.y - npc_rect.y):
            self.moving, self.direction = True, 3
            self.change_animation('walk_down')
        if old_position[1] > self.position[1] and abs(target_rect.x - npc_rect.x) < abs(target_rect.y - npc_rect.y):
            self.moving, self.direction = True, 1
            self.change_animation('walk_up')
        
        
    def move(self) -> None:
        """Définie la trajectoire des NPCS basiques
        
        Args:
            La fonction ne prends aucun argument

        Returns :
            La fonction ne retourne rien --> None 
        """
        
        # print(self.points[0], self.points[-1])
        
        
        current_point = self.current_point
        target_point = self.current_point + self.path_direction
        if target_point >= self.nb_points and self.path_direction == 1:
            target_point = self.nb_points - 2
            self.path_direction = -1
        elif target_point <= 0 and self.path_direction == -1:
            current_point = self.current_point + 1
            self.path_direction = 1
        

        # print(target_point)
        current_rect = self.points[current_point]
        target_rect = self.points[target_point]
        
        
        dx, dy = (target_rect.x + (target_rect.width / 2) - self.rect.centerx , target_rect.y + (target_rect.height / 2) - self.rect.centery)
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        old_position = [self.position[0], self.position[1]]
        self.position[0] += dx * (self.speed / 1.3)
        self.position[1] += dy * (self.speed / 1.3)
        self.animate_npc(old_position, self.rect, target_rect)
        
        if self.rect.colliderect(target_rect):
            self.current_point = target_point
        

    def teleport_spawn(self) -> None:
        """Place le NPC sur le point de spawn de la dernière position (ou de la position de base si 1ère partie)

        Args:
            La fonction ne prends aucun argument

        Returns :
            La fonction ne retourne rien --> None
        """
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location() #Enregistre la localisation
        
    def set_path_coordinates(self, coordinates_list) -> list[list[int]]:
        self.coordinates_list = coordinates_list
        
    def load_points(self, points_list) -> None:
        """Charge les points de trajectoires des NPCS Basiques

        Args:
            tmx_data (_type_): données dans les fichier maps tmx

        Returns :
            La fonction ne retourne rien --> None
        """
        # for num in range(1, self.nb_points+1):
        #     point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
        #     rect = py.Rect(point.x, point.y, point.width, point.height)
        #     rect.center = (point.x + (point.width / 2), point.y + (point.height / 2))
        #     self.points.append(rect)
        
        for num in points_list:
            # print(len(points_list))
            rect = py.Rect(num[1] * 16, num[0] * 16 , 10, 10)
            rect.center = (num[1] * 16 + 5, num[0] * 16 + 5)
            self.points.append(rect)
            
            
class ShopNPC(NPC):
    def __init__(self, x : int, y : int, sprite : str) -> None:
        super().__init__(x, y, sprite)
        
        