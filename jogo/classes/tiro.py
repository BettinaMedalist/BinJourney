import pygame
from classes.game_object import *
from constantes import *

class Tiro(GameObject):
    def __init__(self, screen, player):
        super().__init__(screen, "jogo/sprites/bala.png")

        self.original_image = self.image
        
        self.direction = pygame.math.Vector2(1, 0).rotate(-player.angle)

        self.speed = 1000
        self.velocity = self.direction * self.speed

        self.image = pygame.transform.rotate(self.original_image, -player.angle)

        self.rect = self.image.get_rect(center=player.rect.center)

        self.pos = pygame.math.Vector2(self.rect.center)

    def update(self, delta_time):
        self.pos += self.velocity * delta_time
        self.rect.center = self.pos

        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()