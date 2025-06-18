from classes.game_object import*
from constantes import*

class Tiro(GameObject):
    def __init__(self, screen, image_path, player):
        super().__init__(screen, image_path)
        self.speedx = 0
        self.speedy = 0
        self.speed = 1000
        if player.angle == DIREITA:
            self.rect.centery = player.rect.centery
            self.rect.left = player.rect.right - 50
            self.speedx = self.speed
        elif player.angle == CIMA:
            self.rect.centerx = player.rect.centerx
            self.rect.bottom = player.rect.top + 50
            self.speedy = -self.speed
        elif player.angle == ESQUERDA:
            self.rect.centery = player.rect.centery
            self.rect.right = player.rect.left + 50
            self.speedx = -self.speed
        elif player.angle == BAIXO:
            self.rect.centerx = player.rect.centerx
            self.rect.top = player.rect.bottom - 50
            self.speedy = self.speed
    
    def update(self, delta_time):
        self.rect.x += self.speedx * delta_time
        self.rect.y += self.speedy * delta_time
