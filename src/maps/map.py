from dataclasses import dataclass
import pygame as py
import pytmx, pyscroll

from objects.tiled_entity import TiledEntity
from entities.player import Player
from entities.npc import Basicnpc, ShopNPC
from database_management import JsonManagement as JM


@dataclass
class Portal:
    from_world : str
    origin_point : str 
    target_world : str
    teleport_point : str 

@dataclass
class Map:
    name : str
    walls : list
    group : pyscroll.PyscrollGroup
    tmx_data : pytmx.TiledMap
    portals : list
    npcs : list
    shops : list
    

class MapManager:
    def __init__(self, screen: int, player : str, ennemies_list):
        self.screen = screen
        self.player = player
        self.ennemies_list = ennemies_list
        self.maps = dict()
        self.current_map = JM.get_specific_information('["player"]["current_world"]')
        self.map_collisions_list = [[0] * 250 for _ in range(250)]
        self.inhabitants_list = ["Amelia", "Ash", "Bruce", "Bouncer","Conference_man"
                                , "Dan", "Jack", "Conference_woman", "James"]
        self.points_list = [[[132, 22], [186, 123]], [[90, 144], [225, 88]], [[233, 168], [118, 30]],
                            [[188, 132], [234, 13]], [[164, 229], [92, 19]], [[195, 95], [133, 237]],
                            [[131, 22], [106, 113]], [[183, 148], [118, 98]], [[129, 144], [223, 153]]]
        self.path_list = []

        for name, pos in zip(self.inhabitants_list, self.points_list):
            print(pos[0],pos[1])

        
        self.register_map("World_Alpha", npcs=[
            Basicnpc(name, self.path_length(pos[0], pos[1])) for name, pos in zip(self.inhabitants_list, self.points_list)
        ])

        
        count = 0
        for sprite in self.get_group().sprites():
            if isinstance(sprite, Basicnpc):
                path = self.check_shortest_path(self.map_collisions_list, self.points_list[count][0], self.points_list[count][1], 1, self.heuristic(self.map_collisions_list, self.points_list[count][1]))[0]
                sprite.set_path_coordinates(path)
                self.path_list.append(path)
                count += 1

        
        if self.current_map == "World_Alpha":
            self.player.position[0], self.player.position[1] = Player.get_position()
            self.player.save_location()  
        else:
            self.teleport_player('player')
        self.teleport_npcs()
        
        
            
    # def check_npc_collisions(self, dialog_box):
    #     for sprite in self.get_group().sprites():
    #         if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
    #             dialog_box.execute(sprite.dialog)
        
    def check_collisions(self) -> None:
        """Vérifie si il ya collision ou non 

        Args:
            La fonction ne prends aucun argument --> None

        Returns :
            La fonction ne retourne rien --> None
        """
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = py.Rect(point.x, point.y, point.width, point.height)
                
                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.change_map()
                    self.teleport_player(copy_portal.teleport_point)
                    
                    
        for sprite in self.get_group().sprites():
            if type(sprite) is Basicnpc:
                # if sprite.feet.colliderect(self.player.rect):
                #     sprite.speed = 0
                #     sprite.moving = False
                # else:
                #     sprite.speed = 4
                #     sprite.moving = True
                sprite.speed = sprite.moving = not sprite.feet.colliderect(self.player.rect)
            if not isinstance(sprite, TiledEntity):
                if sprite.feet.collidelist(self.get_walls()) > - 1:
                    sprite.move_back()
                    
    def path_length(self, start_point, end_point):
        """Calcule la longueur du chemin entre deux points

        Args:
            start_point (tuple): Coordonnées du point de départ
            end_point (tuple): Coordonnées du point d'arrivée

        Returns:
            La fonction retourne la longueur du chemin entre deux points --> int
        """
        return len(self.check_shortest_path(self.map_collisions_list, start_point, end_point, 1, self.heuristic(self.map_collisions_list, end_point))[0])
                    
    def check_shortest_path(self, grid, init, goal, cost, heuristic):
        """Retourne le chemin le plus court dans une grille 2d d'un point
        init à un point goal

        Args:
            grid (list): grille
            init (tuple): position de départ
            goal (tuple): position d'arrivée
            cost (int): fonction de coût
            heuristic (list[list[int]]): liste d'estimation

        Returns:
            tuple[list[list[int]], list[list[int]]]: chemin le plus court
        """
        
        DIRECTIONS = [
            [-1, 0],  # left
            [0, -1],  # down
            [1, 0],  # right
            [0, 1],  # up
        ]
        
        closed = [
            [0 for col in range(len(grid[0]))] for row in range(len(grid))
        ]  # the reference grid
        closed[init[0]][init[1]] = 1
        action = [
            [0 for col in range(len(grid[0]))] for row in range(len(grid))
        ]  # the action grid

        x = init[0]
        y = init[1]
        g = 0
        f = g + heuristic[x][y]  # cost from starting cell to destination cell
        cell = [[f, g, x, y]]

        found = False  # flag that is set when search is complete
        resign = False  # flag set if we can't find expand

        while not found and not resign:
            if len(cell) == 0:
                raise ValueError("Algorithm is unable to find solution")
            else:  # to choose the least costliest action so as to move closer to the goal
                cell.sort()
                cell.reverse()
                next = cell.pop()
                x = next[2]
                y = next[3]
                g = next[1]

                if x == goal[0] and y == goal[1]:
                    found = True
                else:
                    for i in range(len(DIRECTIONS)):  # to try out different valid actions
                        x2 = x + DIRECTIONS[i][0]
                        y2 = y + DIRECTIONS[i][1]
                        if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]):
                            if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                                g2 = g + cost
                                f2 = g2 + heuristic[x2][y2]
                                cell.append([f2, g2, x2, y2])
                                closed[x2][y2] = 1
                                action[x2][y2] = i
        invpath = []
        x = goal[0]
        y = goal[1]
        invpath.append([x, y])  # we get the reverse path from here
        while x != init[0] or y != init[1]:
            x2 = x - DIRECTIONS[action[x][y]][0]
            y2 = y - DIRECTIONS[action[x][y]][1]
            x = x2
            y = y2
            invpath.append([x, y])

        path = []
        for i in range(len(invpath)):
            path.append(invpath[len(invpath) - 1 - i])
        return path, action
    
    def heuristic(self, grid, goal):
        heuristic = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                heuristic[i][j] = abs(i - goal[0]) + abs(j - goal[1])
                if grid[i][j] == 1:
                    # added extra penalty in the heuristic map
                    heuristic[i][j] = 99
        return heuristic
        
        
    def teleport_player(self, name : str) -> None:
        """Teleporte le joueur

        Args:
            name (str): nom du joueur

        Returns :
            La fonction ne retourne rien --> None
        """
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()  
        
    def register_map(self, name : str, portals=[] , npcs=[], shops=[]) -> None:
        """Boucle principale générant les principales intervenants de la map

        Args:
            name (str): nom de la map
            portals (list, optional): portails présents sur la map. Defaults to [].
            npcs (list, optional): npcs présents sur la map. Defaults to [].
            shops (list, optional): shops présents sur la map. Defaults to [].

        Returns :
            La fonction ne retourne rien --> None
        """
        # charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame(f'Maps/{name}.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.change_zoom(self.screen.get_width(), self.screen.get_height())
        
        
        
        # definir une liste qui va stocker les rectangles de collisions
        walls = []
        AnimatedTile = []
        
        
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.pytmx.TiledTileLayer):
                    for tile in layer.tiles():
                        if 'collisions' in layer.name:
                            walls.append(py.Rect(tile[0] * tile[2].get_width(), tile[1] * tile[2].get_height(), tile[2].get_width(), tile[2].get_height()))
                            try:
                                self.map_collisions_list[tile[1]][tile[0]] = self.map_collisions_list[tile[1]][tile[0] + 1] = self.map_collisions_list[tile[1]][tile[0] - 1] = self.map_collisions_list[tile[1] + 1][tile[0]] = self.map_collisions_list[tile[1] - 1][tile[0]] = 1
                            except IndexError:
                                self.map_collisions_list[tile[1]][tile[0]] = 1
                        if layer.name == "roads":
                            self.map_collisions_list[tile[1]][tile[0]] = 1
        
        # for obj in tmx_data.objects:
        #     if obj.type == "test":
        #         AnimatedTile.append(TiledEntity(obj.x, obj.y, obj.name, obj.width, obj.height, 4, 5))
        
        # dessiner le groupe de calque
        group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=11)
        for b in AnimatedTile:
            group.add(b)
        group.add(self.player)
        group.add(self.ennemies_list)
        group.add(npc for npc in npcs)
        
        
        for npc in npcs:
            group.add(npc)
        
        # creer un objet map
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs, shops)
        
    def change_zoom(self, width: int, height: int) -> dict:
        """Change le zomm en fonction du pleine écran ou non

        Args:
            width (int): dimension de le fenetre en largeur
            height (int): dimension de le fenetre en hauteur

        Returns:
            dict: le zomm de la map
        """
        self.map_layer.zoom = 5.6 - ((width + height) / 720)
        return self.map_layer
    
        
    def get_map(self) -> dict:
        """Retourne la map actuelle

        Args:
            La fonction ne prends aucun argument --> None

        Returns:
            dict: map actuel
        """
        return self.maps[self.current_map]
    
    def get_group(self) -> dict:
        """Retourne groupe de calques

        Args:
            La fonction ne prends aucun argument --> None

        Returns:
            dict: groupe de calques
        """
        return self.get_map().group
    
    def get_walls(self) -> dict:
        """Retourne groupe de murs

        Args:
            La fonction ne prends aucun argument --> None

        Returns:
            dict: groupe de murs
        """
        return self.get_map().walls
    
    def get_object(self, name: str) -> dict:
        """Recoit les objets par nom depuis le fichier tmx

        Args:
            name (str): nom des objets

        Returns:
            dict: objets et leurs noms
        """
        return self.get_map().tmx_data.get_object_by_name(name)
    
    def teleport_npcs(self) -> None:
        """Teleporte les PNJ

        Args:
            La fonction ne prends aucun argument --> None

        Returns :
            La fonction ne retourne rien --> None
        """
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs
            
            for index, npc in enumerate(npcs):
                npc.load_points(self.path_list[index])
                npc.teleport_spawn()
    
    def draw(self) -> None:
        """Dessine la map

        Args:
            La fonction ne prends aucun argument --> None

        Returns :
            La fonction ne retourne rien --> None
        """
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)
        
    def change_map(self) -> None:
        """Change la map

        Args:
            La fonction ne prends aucun argument --> None

        Returns :
            La fonction ne retourne rien --> None
        """
        world = JM.open_file("saves")
        
        world["player"]["current_world"] = self.current_map
        
        JM.write_file("saves", world)
        
    def update(self) -> None:
        """Met a jour la map avec les npc

        Args:
            La fonction ne prends aucun argument --> None

        Returns :
            La fonction ne retourne rien --> None
        """
        self.get_group().update()
        self.check_collisions()
        
        for npc in self.get_map().npcs:
            npc.move()