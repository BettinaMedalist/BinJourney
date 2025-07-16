from classes.game_object import*

import pygame

class Botao:
    def __init__(self, screen, image_path):
        self.screen = screen
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()

    def draw(self):
        self.screen.blit(self.image, self.rect)

    # SUBSTITUA o método 'apertado' por este:
    def handle_event(self, event):
        """Verifica se o evento de clique ocorreu neste botão."""
        # Verifica se o evento foi um clique com o botão esquerdo do mouse
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Verifica se o clique foi dentro da área do botão
            if self.rect.collidepoint(event.pos):
                return True
        return False