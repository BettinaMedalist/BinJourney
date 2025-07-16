# Arquivo: classes/tiro.py (Substitua todo o conteúdo por este)

from classes.game_object import*
from constantes import*
import math # Importa a biblioteca de matemática

class Tiro(GameObject):
    # O parâmetro foi renomeado para 'owner' (dono) para ser mais genérico
    def __init__(self, screen, owner):
        super().__init__(screen, "jogo/sprites/bala.png")
        self.speed = 1000
        self.original_image = self.image

        # --- LÓGICA DE MOVIMENTO E ROTAÇÃO CORRIGIDA ---

        # 1. Calcula a velocidade usando trigonometria com base no ângulo do "dono".
        #    Isso funciona para QUALQUER ângulo, não apenas para as 4 direções.
        angle_rad = math.radians(owner.angle)
        self.speedx = math.cos(angle_rad) * self.speed
        self.speedy = -math.sin(angle_rad) * self.speed # Eixo Y do Pygame é invertido

        # 2. Rotaciona a imagem da bala para o ângulo correto.
        #    Como esta linha agora é executada sempre, o erro "UnboundLocalError" é resolvido.
        self.image = pygame.transform.rotate(self.original_image, owner.angle)
        self.rect = self.image.get_rect()

        # 3. Posiciona a bala no centro de quem atirou (seja jogador ou inimigo).
        self.rect.center = owner.rect.center

    def update(self, delta_time):
        self.rect.x += self.speedx * delta_time
        self.rect.y += self.speedy * delta_time