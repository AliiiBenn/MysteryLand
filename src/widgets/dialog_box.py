import pygame as py

class DialogBox:
    X_POSITION = 60
    Y_POSITION = 470
    def __init__(self):
        self.box = py.image.load('img/dialog_box.png')
        self.box = py.transform.scale(self.box, (1100, 100))
        self.texts = []
        self.text_index = 0
        self.letter_index = 0
        self.font = py.font.Font('img/dialog_font.ttf', 18)
        self.reading = False
        
    def execute(self, dialog=[]):
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0
            self.texts = dialog
        
    def render(self, screen):
        if self.reading:
            self.letter_index += 1
            
            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index
                
            box_width = screen.get_width() // 2 - (screen.get_width() - 100) // 2
            self.box = py.transform.scale(self.box, (screen.get_width() - 100, 100))
            # on affiche la boite de dialogue centrée en x et à 100 px de haut en y (-150 car -50 + la taille de la boite de dialogue)
            screen.blit(self.box, (box_width, screen.get_height() - 150))
            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0, 0, 0))
            screen.blit(text, (box_width + 80, screen.get_height() - (100 + text.get_height() // 2)))
            
    def next_text(self):
        self.text_index += 1
        self.letter_index = 0
        
        if self.text_index >= len(self.texts):
            self.reading = False