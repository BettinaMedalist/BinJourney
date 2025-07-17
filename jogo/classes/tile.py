import pygame

class Tile(pygame.sprite.Sprite):
    """
    Representa uma única peça visual do cenário (chão ou parede).
    É um sprite simples que só precisa de uma imagem e uma posição.
    """
    def __init__(self, image, x, y, groups):
        # Adiciona este tile a todos os grupos passados na sua criação
        super().__init__(groups)
        
        # Define a aparência visual
        self.image = image
        
        # Cria o retângulo e o posiciona no mapa
        self.rect = self.image.get_rect(topleft=(x, y))