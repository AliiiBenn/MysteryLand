import math
from dataclasses import dataclass

@dataclass
class Checkpoint:
    x : int
    y : int
    width : int
    height : int
    name : str

class Checkpoints:
    def get_checkpoints(tmx_data):
        checkpoints_list = []
        for obj in tmx_data.objects:
            if not obj.name is None and "checkpoint" in obj.name:
                checkpoints_list.append(Checkpoint(obj.x, obj.y, obj.width, obj.height, obj.name))
        return checkpoints_list
    
    @staticmethod
    def check_checkpoint_distance(entity, checkpoint : Checkpoint) -> float:
        """Retourne la distance entre deux points avec leurs positions en x et en y

        Args:
            entity (Entity): L'entitée qui va être téléportée
            checkpoint (Checkpoint): Le checkpoint cible

        Returns:
            float: la distance entre l'entitée et le checkpoint
        """
        dx, dy = entity.rect.x - checkpoint.x, entity.rect.y - checkpoint.y
        return math.hypot(dx, dy)
    
    @staticmethod
    def check_closest_checkpoint(entity, checkpoint_list) -> Checkpoint:
        """Regarde quel est le checkpoint le plus proche du joueur et le retourner

        Args:
            entity (Entity): L'entitée qui va être téléportée
            checkpoint_list (list[Checkpoint]): liste des checkpoints de la map

        Returns:
            Checkpoint: Le checkpoint le plus proche
        """
        closest_checkpoint = None
        closest_checkpoint_distance = 0
        for checkpoint in checkpoint_list:
            distance = Checkpoints.check_checkpoint_distance(entity, checkpoint)
            if closest_checkpoint is None or distance < closest_checkpoint_distance:
                closest_checkpoint = checkpoint
                closest_checkpoint_distance = distance
        return closest_checkpoint
                
    @staticmethod
    def teleport_to_checkpoints(entity, checkpoint_list) -> None:
        """Téléporte l'entitée au checkpoint le plus proche

        Args:
            entity (Entity): L'entitée qui va être téléportée
            checkpoint_list (list[Checkpoint]): liste des checkpoint de la map
        """
        closest_checkpoint = Checkpoints.check_closest_checkpoint(entity, checkpoint_list)
        entity.position[0], entity.position[1] = closest_checkpoint.x, closest_checkpoint.y

