from classes.game_object import*
import pygame

class HealthDrop(GameObject):
    def __init__(self, screen, x, y):
        super().__init__(screen, "jogo/sprites/life.png", x, y)

        self.rect.center = (x, y)

        self.hitbox = self.rect.copy()
        
        self.creation_time = pygame.time.get_ticks()
        
        self.lifetime = 5000