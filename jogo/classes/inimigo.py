from classes.game_object import*
from constantes import*
from classes.tiro import Tiro
import pygame
import math

ESTADO_PATRULHA = "patrulhando"
ESTADO_ATAQUE = "atacando"
ESTADO_BUSCA = "procurando"
ESTADO_RETORNO = "retornando"
ESTADO_RECARREGANDO = "recarregando"

class Inimigo(GameObject):
    def __init__(self, screen, armed_image_path, angle, x=0, y=0):
        super().__init__(screen, armed_image_path, x, y)

        self.interrogacao = carregar_imagem("jogo/sprites/interrogacao.png")
        self.exclamacao = carregar_imagem("jogo/sprites/exclamacao.png")
        self.icone_estado_atual = None

        self.vidas = 3
        self.angle = angle
        self.original_image = self.image
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(x, y))


        self.estado = ESTADO_PATRULHA
        self.velocidade = 70
        self.alvo_busca = None
        self.tempo_busca = 0
        self.px = x
        self.py = y
        self.ponto_patrulha = (x, y)
        self.vx = 0
        self.vy = 0

        self.raio_visao = 500
        self.angulo_visao = 90
        
        self.shots = []
        self.tempo_disparo = 0
        self.cadencia = 1.5

        self.municao_maxima = 10
        self.municao_atual = self.municao_maxima
        self.tempo_recarga_total = 2.5
        self.tempo_recarga_atual = 0

        self.direcao_scan = 1
        self.angulo_original_scan = 0

    def update(self, player, delta_time):
        self.atualizar_icone_estado()

        self.ponto_patrulha = (self.px, self.py)

        if self.estado == ESTADO_BUSCA or self.estado == ESTADO_ATAQUE:
            self.velocidade = 120
        else:
            self.velocidade = 70

        self.vx = 0
        self.vy = 0

        if self.estado == ESTADO_BUSCA:
            self.buscar(delta_time)
        elif self.estado == ESTADO_ATAQUE:
            self.atacar(player, delta_time)
        elif self.estado == ESTADO_RETORNO:
            self.retornar()
        elif self.estado == ESTADO_RECARREGANDO:
            self.recarregar(delta_time)
        
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.hitbox.center = self.rect.center

    def draw_vision_cone(self):
        """Desenha o cone de visão do inimigo para fins de depuração."""
        # Cria uma lista de pontos para desenhar um polígono que representa o cone
        points = [self.rect.center]
        
        # Calcula os ângulos de início e fim do cone em graus
        start_deg = self.angle - self.angulo_visao / 2
        end_deg = self.angle + self.angulo_visao / 2

        # Gera pontos ao longo do arco do cone de visão
        # Aumentar o número de segmentos deixa o arco mais suave
        for i in range(21): 
            current_angle_deg = start_deg + (end_deg - start_deg) * i / 20
            current_angle_rad = math.radians(current_angle_deg)
            
            # Calcula o ponto na borda do círculo de visão
            px = self.rect.centerx + self.raio_visao * math.cos(current_angle_rad)
            # O eixo Y do Pygame é invertido, por isso o sinal de menos no seno
            py = self.rect.centery - self.raio_visao * math.sin(current_angle_rad) 
            points.append((px, py))
        
        # Desenha o contorno do polígono em amarelo
        pygame.draw.polygon(self.screen, (255, 255, 0), points, 1)

    # Função renomeada para ser genérica
    def pode_ver_alvo(self, alvo):
        dx = alvo.rect.centerx - self.rect.centerx
        dy = alvo.rect.centery - self.rect.centery

        #Calcula a distâcia entre o alvo e o inimigo
        dist = math.hypot(dx, dy)
        
        if dist > self.raio_visao:
            return False

        angulo_para_alvo = math.degrees(math.atan2(-dy, dx))
        diff_angulo = abs(angulo_para_alvo - self.angle)
        diff_angulo = (diff_angulo + 180) % 360 - 180

        if abs(diff_angulo) < self.angulo_visao / 2:
            return True

        return False

    def atirar(self):
        self.municao_atual -= 1
        self.shots.append(Tiro(self.screen, self))

    def definir_movimento_para_alvo(self, alvo):
        direcao_x = alvo[0] - self.rect.centerx
        direcao_y = alvo[1] - self.rect.centery
        dist = math.hypot(direcao_x, direcao_y)

        if dist > 10:
            self.vx = (direcao_x / dist) * self.velocidade
            self.vy = (direcao_y / dist) * self.velocidade
            if abs(direcao_x) > abs(direcao_y):
                self.angle = DIREITA if direcao_x > 0 else ESQUERDA
            else:
                self.angle = BAIXO if direcao_y > 0 else CIMA
            return False
        return True

    def buscar(self, delta_time):     
        if self.alvo_busca:
            if self.definir_movimento_para_alvo(self.alvo_busca):
                self.alvo_busca = None
                self.tempo_busca = 5
                self.angulo_original_scan = self.angle
                self.direcao_scan = 1
        
        if self.tempo_busca > 0:
            self.tempo_busca -= delta_time
            velocidade_scan = 60
            self.angle += velocidade_scan * self.direcao_scan * delta_time

            diff_angulo = self.angle - self.angulo_original_scan
            if abs(diff_angulo) > 45:
                self.direcao_scan *= -1
                
            if self.tempo_busca <= 0:
                self.estado = ESTADO_RETORNO

    def retornar(self):
        if self.definir_movimento_para_alvo(self.ponto_patrulha):
            self.estado = ESTADO_PATRULHA

    def atacar(self, player, delta_time):
        if self.pode_ver_alvo(player):
            self.alvo_busca = list(player.rect.center)
            self.tempo_disparo += delta_time

            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)
        
            if abs(dx) > abs(dy):
                self.angle = DIREITA if dx > 0 else ESQUERDA
            else:
                self.angle = BAIXO if dy > 0 else CIMA
        
            if dist > 150:
                self.definir_movimento_para_alvo(player.rect.center)

            if self.municao_atual > 0:
                if self.tempo_disparo >= self.cadencia:
                    self.atirar()
                    self.tempo_disparo = 0
        
            else:
                self.estado = ESTADO_RECARREGANDO
                self.tempo_recarga_atual = self.tempo_recarga_total
        else:
            if self.alvo_busca:
                vetor_fuga_x = player.rect.centerx - self.alvo_busca[0]
                vetor_fuga_y = player.rect.centery - self.alvo_busca[1]

                # Apenas vira se o jogador realmente se moveu desde a última vez que foi visto
                if vetor_fuga_x != 0 or vetor_fuga_y != 0:
                    # Determina a direção principal da fuga e ajusta o ângulo do inimigo
                    if abs(vetor_fuga_x) > abs(vetor_fuga_y):
                        self.angle = DIREITA if vetor_fuga_x > 0 else ESQUERDA
                    else:
                        self.angle = BAIXO if vetor_fuga_y > 0 else CIMA
                # Se o jogador não se moveu (apenas se escondeu), o inimigo olha para a última posição dele
                else:
                    dx = self.alvo_busca[0] - self.rect.centerx
                    dy = self.alvo_busca[1] - self.rect.centery
                    if abs(dx) > abs(dy):
                        self.angle = DIREITA if dx > 0 else ESQUERDA
                    else:
                        self.angle = BAIXO if dy > 0 else CIMA

            self.estado = ESTADO_BUSCA

    def recarregar(self, delta_time):
        self.vx = 0
        self.vy = 0

        self.tempo_recarga_atual -= delta_time
        if self.tempo_recarga_atual <= 0:
            self.municao_atual = self.municao_maxima
            self.estado = ESTADO_ATAQUE

    def atualizar_icone_estado(self):
        if self.estado == ESTADO_BUSCA:
            self.icone_estado_atual = self.interrogacao
        elif self.estado == ESTADO_ATAQUE:
            self.icone_estado_atual = self.exclamacao
        else:
            self.icone_estado_atual = None

class Inimigo_Pistola(Inimigo):
    def __init__(self, screen, angle, x, y):
        super().__init__(screen, "jogo/sprites/inimigo_pistola.png", angle, x, y)
        self.hitbox = self.rect.inflate(-100, -100)
        self.cadencia = 1.5
        self.municao_maxima = 10
        self.municao_atual = self.municao_maxima

class Inimigo_Metralhadora(Inimigo):
    def __init__(self, screen, angle, x, y):
        super().__init__(screen, "jogo/sprites/inimigo_metralhadora.png", angle, x, y)
        self.hitbox = self.rect.inflate(-50, -50)
        self.cadencia = 0.2
        self.municao_maxima = 30
        self.municao_atual = self.municao_maxima

class Inimigo_Pistola_Patrulha(Inimigo_Pistola):
    def __init__(self, screen, angle, x, y, ponto_b):
        super().__init__(screen, angle, x, y)
        self.ponto_a = (x, y)
        self.ponto_b = ponto_b
        self.alvo_patrulha_atual = self.ponto_b
    
    def update(self, player, delta_time):
        """Sobrescreve o update para adicionar o comportamento de patrulha."""
        self.atualizar_icone_estado()

        # Define a velocidade baseada no estado
        if self.estado == ESTADO_BUSCA or self.estado == ESTADO_ATAQUE:
            self.velocidade = 120
        else:
            self.velocidade = 70

        self.vx = 0
        self.vy = 0

        # Lógica de estados
        if self.estado == ESTADO_PATRULHA:
            self.patrulhar()
        elif self.estado == ESTADO_BUSCA:
            self.buscar(delta_time)
        elif self.estado == ESTADO_ATAQUE:
            self.atacar(player, delta_time)
        elif self.estado == ESTADO_RETORNO:
            self.retornar_a_patrulha() # Usa um método de retorno customizado
        elif self.estado == ESTADO_RECARREGANDO:
            self.recarregar(delta_time)
        
        # Atualiza a imagem e posição
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.hitbox.center = self.rect.center

    def patrulhar(self):
        """Move o inimigo em direção ao seu ponto de patrulha atual."""
        # Se chegou ao destino, troca o alvo da patrulha
        if self.definir_movimento_para_alvo(self.alvo_patrulha_atual):
            if self.alvo_patrulha_atual == self.ponto_a:
                self.alvo_patrulha_atual = self.ponto_b
            else:
                self.alvo_patrulha_atual = self.ponto_a
    
    def retornar_a_patrulha(self):
        """Ao invés de retornar a um ponto fixo, retorna ao ponto mais próximo da patrulha."""
        # Calcula a distância para ambos os pontos da patrulha
        dist_a = math.hypot(self.rect.centerx - self.ponto_a[0], self.rect.centery - self.ponto_a[1])
        dist_b = math.hypot(self.rect.centerx - self.ponto_b[0], self.rect.centery - self.ponto_b[1])

        # Define o alvo como o ponto mais próximo
        ponto_retorno = self.ponto_a if dist_a < dist_b else self.ponto_b
        self.alvo_patrulha_atual = ponto_retorno # Garante que a patrulha continue dali

        if self.definir_movimento_para_alvo(ponto_retorno):
            self.estado = ESTADO_PATRULHA

# REMOVA a classe Inimigo_Melee_Patrulha e a Inimigo_Pistola_Patrulha se quiser
# E ADICIONE esta classe no lugar.

class Inimigo_Melee(Inimigo):
    """Um inimigo desarmado que fica parado e ataca corpo a corpo ao ver o jogador."""
    def __init__(self, screen, angle, x, y):
        # Inicia com o sprite de inimigo desarmado
        super().__init__(screen, "jogo/sprites/inimigo_semarma.png", angle, x, y)
        
        # Atributos de combate
        self.velocidade_corrida = 180 # Velocidade ao atacar/buscar
        self.alcance_ataque = 60
        self.dano = 1
        self.cooldown_ataque = 1.2
        self.tempo_ultimo_ataque = 0

    def update(self, player, delta_time):
        """Controla a lógica de estados: patrulha (parado), busca e ataque."""
        self.atualizar_icone_estado()

        # Ajusta a velocidade baseada no estado
        if self.estado == ESTADO_BUSCA or self.estado == ESTADO_ATAQUE:
            self.velocidade = self.velocidade_corrida
        else:
            self.velocidade = 70

        self.vx = 0
        self.vy = 0

        # Máquina de estados. Note que não há chamada para "patrulhar".
        # Quando em ESTADO_PATRULHA, ele simplesmente não faz nada, ficando parado.
        if self.estado == ESTADO_BUSCA:
            self.buscar(delta_time)
        elif self.estado == ESTADO_ATAQUE:
            self.atacar(player, delta_time)
        elif self.estado == ESTADO_RETORNO:
            self.retornar() # Usa o método 'retornar' da classe base para voltar ao posto

        # Atualiza a imagem e posição
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.hitbox.center = self.rect.center

    def atirar(self):  # Este inimigo não atira
        pass

    def recarregar(self, delta_time):  # Nem recarrega
        pass

    def atacar(self, player, delta_time):
        """Persegue e ataca o jogador corpo a corpo."""
        # Se não pode mais ver o jogador, muda para o estado de busca
        if not self.pode_ver_alvo(player):
            self.estado = ESTADO_BUSCA
            return

        # Persegue o jogador
        self.definir_movimento_para_alvo(player.rect.center)
        
        dist_jogador = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)
        
        # Estando no alcance, ataca
        tempo_atual = pygame.time.get_ticks() / 1000
        if dist_jogador <= self.alcance_ataque:
            if tempo_atual - self.tempo_ultimo_ataque > self.cooldown_ataque:
                player.sofrer_dano(self.dano)
                self.tempo_ultimo_ataque = tempo_atual