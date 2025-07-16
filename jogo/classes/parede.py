import pygame
from constantes import TILE_SIZE # Importe TILE_SIZE


class Parede(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)