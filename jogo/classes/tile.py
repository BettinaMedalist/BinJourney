import pygame
from constantes import*
from classes.game_object import GameObject

# A classe Tile herda de GameObject, então já é um Sprite.
# Ela é usada para construir os elementos estáticos do cenário (paredes, chão).
class Tile(GameObject):
    def __init__(self, image, x, y, groups, layer=0):
        # Não precisamos de um caminho de imagem, pois a imagem já virá carregada.
        super().__init__(screen=None) # A tela não é necessária aqui.
        self.image = image
        self._layer = layer
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.copy()
        
        # Adiciona este tile a todos os grupos fornecidos.
        # Isso é crucial para o desenho e a colisão.
        for group in groups:
            group.add(self)