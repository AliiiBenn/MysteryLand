import pygame as py
from .entity import Entity
from database_management.json_management import JsonManagement as JM
from database_management.database_link import DatabaseLink

class Player(Entity):
    def __init__(self, x, y, life):
        super().__init__(x, y, "Adam")
        self.life = self.get_life()
        if self.life == None or self.life == 0:
            self.change_player_life(life)
        
    @staticmethod
    def get_position():
        """obtient la position du joueur

        Returns:
            _type_: position du joueur
        """
        f = JM.open_file("saves")
        player_position = JM.get_specific_information('["player"]["position"]')
        return player_position
    
    def change_player_position(self):
        """change la position du joueur
        """
        current_player_position = [self.rect.x, self.rect.y]
        player_p = JM.open_file("saves")
        
        player_p["player"]["position"] = current_player_position
        
        JM.write_file('saves', player_p)
        
    @staticmethod
    def get_life() -> int:
        """va chercher la vie du joueur dans le fichier save et la return

        Returns:
            _type_: retourne la vie acuel du joueur
        """
        f = JM.open_file("saves")
        life = JM.get_specific_information('["player"]["life"]')
        return life
    
    def change_player_life(self, life: int):
        """va écrire dans le fichier save la vie du joueur

        Args:
            life (int): vie du joueur entre 0 et 100
        """
        player_l = JM.open_file("saves")
        
        player_l["player"]["life"] = life
        
        JM.write_file('saves', player_l)
        
    def is_player_dead(self):
        """voit si le joueur est mort

        Returns:
            _type_: 0 si mort, life <= 0
                    1 si vivant, life > 0
        """
        return self.life <= 0
    
class PlayerInformation(DatabaseLink):
    def __init__(self):
        super().__init__()
        
    
    def update_user_informations(self, user_name: str, dungeons: int, money: int, level: int, xp: int):
        """_summary_

        Args:
            user_name (str): nom du joueur
            dungeons (int): numéro du donjon
            money (int): quantité d'argent
            level (int): nombre de level
            xp (int): nombre d'xp

        Returns:
            _type_: return les informations concernant le joueur 
        """
        return self.users_ref.update({
            user_name : {
                'nickname' : user_name,
                'dungeons' : dungeons,
                'money' : money,
                'level' : [level, xp]
            }
        })
        
    def get_json_informations(self):
        """obtient les informations depuis le json

        Returns:
            _type_: return les information précise concernant le joueur, méthode utilisée par les autres en haut
        """
        return JM.get_specific_information('["player"]["database_data"]')
