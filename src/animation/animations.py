import pygame as py


class Animations:
    def __init__(self, player, screen):
        self.player = player
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        self.screen_animation_finished = False
        self.distance = 0

    def teleport_player(self, destination : list[int]) -> None:
        """Méthode permettant de téléporter le joueur à une position donnée pour lancer l'animation

        Args:
            destination (list[int]): la liste des positions x et y du joueur
        """
        self.player.position[0] = destination[0]
        self.player.position[1] = destination[1]

    def screen_animation(self, screen):
        self.distance += 5
        py.draw.rect(screen, (0, 0, 0), (0 - self.distance, 0, self.width // 2, self.height))
        py.draw.rect(screen, (0, 0, 0), (self.width // 2 + self.distance, 0, self.width, self.height))
        if self.distance >= self.width // 2:
            self.screen_animation_finished = True
            self.width, self.height = self.screen.get_size()
            return self.screen_animation_finished
        