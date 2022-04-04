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
        """Obtient la position du joueur

        Args:
            La fonction ne prends aucun argument --> None

        Returns:
            _type_: position du joueur
        """
        f = JM.open_file("saves")
        player_position = JM.get_specific_information('["player"]["position"]')
        return player_position
    
    def change_player_position(self):
        """Change la position du joueur

        Args:
            La fonction ne prends aucun argument

        Returns :
            La fonction ne retourne rien --> None
        """
        current_player_position = [self.rect.x, self.rect.y]
        player_p = JM.open_file("saves")
        
        player_p["player"]["position"] = current_player_position
        
        JM.write_file('saves', player_p)
        
    @staticmethod
    def get_life() -> int:
        """Cherche la vie du joueur dans le fichier "saves.json" et la return

        Args:
            La fonction ne prends aucun argument

        Returns:
            _type_: retourne la vie acuel du joueur
        """
        f = JM.open_file("saves")
        life = JM.get_specific_information('["player"]["life"]')
        return life
    
    def change_player_life(self, life: int):
        """Ecrit dans le fichier "saves.json" la vie du joueur

        Args:
            life (int): vie du joueur entre 0 et 100
            
        Returns :
            La fonction ne retourne rien --> None
        """
        player_l = JM.open_file("saves")
        
        player_l["player"]["life"] = life
        
        JM.write_file('saves', player_l)
        
    def is_dead(self):
        """Vérifie si le joueur est mort

        Args:
            La fonction ne prends aucun argument

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
        """Obtient les informations depuis le json

        Args:
            La fonction ne prends aucun argument
            
        Returns:
            _type_: return les information précise concernant le joueur, méthode utilisée par les autres en haut
        """
        return JM.get_specific_information('["player"]["database_data"]')


class NewPlayer:
    def __init__(self, player):
        self.player = player
        
    def create_new_player_informations(nickname, player_informations):
        """Créer un nouveau joueur dans le fichier saves.json

        Args:
            nickname (str): le nom du joueur

        Returns :
            La fonction ne retourne rien --> None
        """
        player = JM.open_file('saves')
        
        player["player"].update({
            "position" : [0, 0],
            "life" : 100,
            "current_world" : "World_Alpha",
            "database_data" : {
                "dungeons" : 0,
                "nickname" : nickname,
                "money" : 0,
                "level" : [0, 0],
                "quests" : {
                    
                }
            }
            
        })
        
        player_informations.update_user_informations(nickname, 0, 0, 0, 0)
        JM.write_file('saves', player)