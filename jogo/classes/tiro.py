from classes.game_object import*
from constantes import*

class Tiro(GameObject):
    def __init__(self, screen, player):
        super().__init__(screen, "jogo/sprites/bala.png")
        self.speedx = 0
        self.speedy = 0
        self.speed = 1000
        self.original_image = self.image
        if player.angle == DIREITA:
            self.rect.centery = player.rect.centery
            self.rect.left = player.rect.right - 50
            self.speedx = self.speed
            rotated_image = pygame.transform.rotate(self.original_image, DIREITA)
        elif player.angle == CIMA:
            self.rect.centerx = player.rect.centerx
            self.rect.bottom = player.rect.top + 50
            self.speedy = -self.speed
            rotated_image = pygame.transform.rotate(self.original_image, CIMA)
        elif player.angle == ESQUERDA:
            self.rect.centery = player.rect.centery
            self.rect.right = player.rect.left + 50
            self.speedx = -self.speed
            rotated_image = pygame.transform.rotate(self.original_image, ESQUERDA)
        elif player.angle == BAIXO:
            self.rect.centerx = player.rect.centerx
            self.rect.top = player.rect.bottom - 50
            self.speedy = self.speed
            rotated_image = pygame.transform.rotate(self.original_image, BAIXO)

        self.image = rotated_image
    
    def update(self, delta_time):
        self.rect.x += self.speedx * delta_time
        self.rect.y += self.speedy * delta_time
