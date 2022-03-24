import pygame as py


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.FONT = py.font.SysFont('Corbel', 75)
        self.color = (0, 0, 0)
        self.rect = py.Rect(x, y, w, h)
        self.rect.center = (x, y)
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event) -> list:
        """Méthode principale qui va gérer l'affichage du texte et la touche entrer

        Args:
            event (py.event): liste des evenements pygame

        Returns:
            list: renvoie une liste avec un booleen et le texte
        """
        if event.type == py.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
        if event.type == py.KEYDOWN:
            if self.active:
                if event.key == py.K_RETURN:
                    return [True, self.text]
                elif event.key == py.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.FONT.render(self.text, True, self.color)

    def update(self, x, y) -> None:
        """Met à jour l'input box

        Args:
            x (int): position en x
            y (int): position en y

        Returns :
            La fonction ne retourne rien --> None
        """
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width 
        self.rect.center = (x, y)

    def draw(self, screen):
        """Créer le bouton 

        Args:
            screen (py.display): l'ecran où l'input box va être affichée

        Returns :
            La fonction ne retourne rien --> None
        """
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        py.draw.rect(screen, self.color, self.rect, 2)    

