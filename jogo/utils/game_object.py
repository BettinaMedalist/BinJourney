import pygame
from utils.funcoes import carregar_imagem

#A maior parte dos sprites do jogo terá essa classe para facilitar a colisão e o posicionamento dos objetos
class GameObject():
    def __init__(self, image_path = None, x = 0, y = 0):
        self.x = x
        self.y = y
        self.image = None
        if image_path:
            self.image = carregar_imagem(image_path)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, tela):
        tela.blit(self.image, (self.x, self.y))
   
