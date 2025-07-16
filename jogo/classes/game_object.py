from utils.funcoes import*
import pygame # Adicione o import do pygame aqui

#A maior parte dos sprites do jogo terá essa classe para facilitar a colisão e o posicionamento dos objetos
class GameObject():
    def __init__(self, screen, image_path = None, x = 0, y = 0):
        self.angle = 0
        self.screen = screen
        self.image = None
        if image_path:
            self.image = carregar_imagem(image_path)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.hitbox = self.rect.copy()

    def draw(self):
        self.screen.blit(self.image, self.rect)
        pygame.draw.rect(self.screen, (255, 0, 0), self.hitbox, 2)