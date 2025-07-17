import pygame
from classes.game_object import *
from constantes import *


class Tiro(GameObject):
    def __init__(self, screen, owner):
        # Inicia o GameObject, carregando a imagem da bala
        super().__init__(screen, "jogo/sprites/bala.png")

        # Guarda a imagem original para rotações limpas
        self.original_image = self.image

        # --- LÓGICA DE VETORES (DA SUA VERSÃO) ---

        # 1. Usa o ângulo do "dono" (seja player ou inimigo) para criar um vetor de direção
        self.direction = pygame.math.Vector2(1, 0).rotate(-owner.angle)

        # 2. Define a velocidade e calcula o vetor de velocidade
        self.speed = 1000
        self.velocity = self.direction * self.speed

        # 3. Rotaciona a imagem da bala para que ela "aponte" para onde vai
        self.image = pygame.transform.rotate(self.original_image, -owner.angle)

        # 4. Posiciona a bala no centro de quem atirou, usando o rect da imagem já rotacionada
        self.rect = self.image.get_rect(center=owner.rect.center)

        # 5. Usa um vetor para a posição para movimento mais preciso com floats
        self.pos = pygame.math.Vector2(self.rect.center)

    def update(self, delta_time):
        # Move a posição precisa (float) da bala
        self.pos += self.velocity * delta_time
        # Atualiza o retângulo de desenho (int) com base na posição precisa
        self.rect.center = self.pos

        # Verifica se a bala saiu da tela para se autodestruir
        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()  # Remove a bala de todos os grupos a que ela pertence