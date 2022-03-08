import pygame as py
from .entity import Entity


class NPC(Entity):
    def __init__(self, x : int, y : int, sprite : str) -> None:
        super().__init__(x, y, sprite)


class Specialnpc(NPC):
    def __init__(self, x : int, y : int, sprite : str) -> None:
        super().__init__(x, y, sprite)
        
class Basicnpc(NPC):
    def __init__(self, sprite : str, nb_points : int) -> None:
        super().__init__(0, 0, sprite)
        self.nb_points = nb_points
        self.points = []
        self.speed = 1
        self.name = sprite
        self.current_point = 0
        
        
    def move(self) -> None:
        """Définie la trajectoire des NPCS basiques
        """
        current_point = self.current_point
        target_point = self.current_point + 1
        
        if target_point >= self.nb_points:
            target_point = 0


        current_rect = self.points[current_point]
        target_rect = self.points[target_point]
        
        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_down()
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_up()
        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_left()
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_right()
            
        if self.rect.colliderect(target_rect):
            self.current_point = target_point

    def teleport_spawn(self) -> None:
        """Place le NPC sur le point de spawn de la dernière position (ou de la position de base si 1ère partie)
        """
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location() #Enregistre la localisation
        
    def load_points(self, tmx_data) -> None:
        """Charge les points de trajectoires des NPCS Basiques

        Args:
            tmx_data (_type_): données dans les fichier maps tmx
        """
        for num in range(1, self.nb_points+1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = py.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)
            
            
class ShopNPC(NPC):
    def __init__(self, x : int, y : int, sprite : str) -> None:
        super().__init__(x, y, sprite)
        
        