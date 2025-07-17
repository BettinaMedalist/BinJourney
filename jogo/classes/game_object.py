from utils.funcoes import*
import pygame

# A classe agora herda de pygame.sprite.Sprite
# Isso permite que qualquer objeto do jogo seja adicionado a um pygame.sprite.Group
class GameObject(pygame.sprite.Sprite):
    def __init__(self, screen, image_path = None, x = 0, y = 0):
        super().__init__() # Inicializa a classe pai Sprite
        self.angle = 0
        self.screen = screen
        self.image = None
        if image_path:
            self.image = carregar_imagem(image_path)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.hitbox = self.rect.copy()

    def draw(self):
        # A lógica de desenho individual é mantida para casos específicos,
        # mas a renderização principal será feita pelo método .draw() do grupo.
        self.screen.blit(self.image, self.rect)
        # Descomente a linha abaixo para depurar hitboxes
        # pygame.draw.rect(self.screen, (255, 0, 0), self.hitbox, 2)