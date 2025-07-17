import pygame
import math
from constantes import *
from classes.game_object import GameObject
from classes.tiro import Tiro
from utils.funcoes import carregar_imagem



class Inimigo(GameObject):
    def __init__(self, screen, image_path, angle, x=0, y=0):
        super().__init__(screen, image_path, x, y)

        self.vidas = 3
        self.angle = angle
        self.original_image = self.image
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = self.rect.inflate(-20, -20) # Hitbox padrão, pode ser sobrescrita

        # Atributos de IA
        self.estado = ESTADO_PATRULHA
        self.velocidade = 70
        self.vx, self.vy = 0, 0
        self.ponto_patrulha_inicial = (x, y)

        # Atributos de Visão e Alerta
        self.raio_visao = 400
        self.angulo_visao = 90
        self.alvo_busca = None
        self.tempo_busca = 0
        self.direcao_scan = 1
        self.angulo_original_scan = 0
        self.icone_estado_atual = None
        self.interrogacao = carregar_imagem("jogo/sprites/interrogacao.png")
        self.exclamacao = carregar_imagem("jogo/sprites/exclamacao.png")
        
        # Atributos de Combate
        self.shots = pygame.sprite.Group()
        self.tempo_disparo = 0
        self.cadencia = 1.5
        self.municao_maxima = 10
        self.municao_atual = self.municao_maxima
        self.tempo_recarga_total = 2.5
        self.tempo_recarga_atual = 0

    def update(self, player, delta_time, enemy_shots_group, walls_group):
        self.atualizar_icone_estado()

        if self.estado == ESTADO_BUSCA or self.estado == ESTADO_ATAQUE:
            self.velocidade = 120
        else:
            self.velocidade = 70

        self.vx, self.vy = 0, 0

        if self.estado == ESTADO_BUSCA:
            self.buscar(delta_time)
        elif self.estado == ESTADO_ATAQUE:
            self.atacar(player, delta_time, enemy_shots_group, walls_group)
        elif self.estado == ESTADO_RETORNO:
            self.retornar()
        elif self.estado == ESTADO_RECARREGANDO:
            self.recarregar(delta_time)
        
        # Aplica o movimento próprio do inimigo
        self.rect.x += self.vx * delta_time
        self.rect.y += self.vy * delta_time
        
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.hitbox.center = self.rect.center

    def pode_ver_alvo(self, alvo, walls_group):
        dist_vec = pygame.math.Vector2(alvo.rect.center) - pygame.math.Vector2(self.rect.center)
        dist = dist_vec.length()

        if dist == 0 or dist > self.raio_visao: return False

        angulo_para_alvo = math.degrees(math.atan2(-dist_vec.y, dist_vec.x))
        diff_angulo = (self.angle - angulo_para_alvo + 180) % 360 - 180

        if abs(diff_angulo) > self.angulo_visao / 2: return False

        for i in range(0, int(dist), 20):
            ponto_verificacao = self.rect.center + dist_vec.normalize() * i
            for wall in walls_group:
                if wall.rect.collidepoint(ponto_verificacao): return False
        return True

    def definir_movimento_para_alvo(self, alvo_pos):
        direcao_vetor = pygame.math.Vector2(alvo_pos) - self.rect.center
        dist = direcao_vetor.length()

        if dist > 10:
            self.angle = math.degrees(math.atan2(-direcao_vetor.y, direcao_vetor.x))
            direcao_vetor.normalize_ip()
            self.vx = direcao_vetor.x * self.velocidade
            self.vy = direcao_vetor.y * self.velocidade
            return False
        return True

    def atirar(self, enemy_shots_group):
        if self.municao_atual > 0:
            self.municao_atual -= 1
            novo_tiro = Tiro(self.screen, self)
            self.shots.add(novo_tiro)
            enemy_shots_group.add(novo_tiro)

    def buscar(self, delta_time):     
        if self.alvo_busca and self.definir_movimento_para_alvo(self.alvo_busca):
            self.alvo_busca = None
            self.tempo_busca = 5
            self.angulo_original_scan = self.angle
            self.direcao_scan = 1
        
        if self.tempo_busca > 0:
            self.tempo_busca -= delta_time
            self.angle += 60 * self.direcao_scan * delta_time
            if abs(self.angle - self.angulo_original_scan) > 45: self.direcao_scan *= -1
            if self.tempo_busca <= 0: self.estado = ESTADO_RETORNO

    def retornar(self):
        if self.definir_movimento_para_alvo(self.ponto_patrulha_inicial):
            self.estado = ESTADO_PATRULHA

    def atacar(self, player, delta_time, enemy_shots_group, walls_group):
        if self.pode_ver_alvo(player, walls_group):
            self.alvo_busca = list(player.rect.center)
            self.tempo_disparo += delta_time
            self.definir_movimento_para_alvo(player.rect.center)
            
            if self.municao_atual > 0:
                if self.tempo_disparo >= self.cadencia:
                    self.atirar(enemy_shots_group)
                    self.tempo_disparo = 0
            else:
                self.estado = ESTADO_RECARREGANDO
                self.tempo_recarga_atual = self.tempo_recarga_total
        else:
            self.estado = ESTADO_BUSCA

    def recarregar(self, delta_time):
        self.tempo_recarga_atual -= delta_time
        if self.tempo_recarga_atual <= 0:
            self.municao_atual = self.municao_maxima
            self.estado = ESTADO_ATAQUE

    def atualizar_icone_estado(self):
        if self.estado == ESTADO_BUSCA: self.icone_estado_atual = self.interrogacao
        elif self.estado == ESTADO_ATAQUE: self.icone_estado_atual = self.exclamacao
        else: self.icone_estado_atual = None

    def sofrer_dano(self, quantidade):
        self.vidas -= quantidade
        if self.vidas <= 0:
            self.kill()

class Inimigo_Pistola(Inimigo):
    def __init__(self, screen, angle, x, y):
        super().__init__(screen, "jogo/sprites/inimigo_pistola.png", angle, x, y)
        self.hitbox = self.rect.inflate(-30, -30)
        self.cadencia = 1.5
        self.municao_maxima = 10
        self.municao_atual = self.municao_maxima

class Inimigo_Metralhadora(Inimigo):
    def __init__(self, screen, angle, x, y):
        super().__init__(screen, "jogo/sprites/inimigo_metralhadora.png", angle, x, y)
        self.hitbox = self.rect.inflate(-30, -30)
        self.cadencia = 0.2
        self.municao_maxima = 30
        self.municao_atual = self.municao_maxima

class Inimigo_Pistola_Patrulha(Inimigo_Pistola):
    def __init__(self, screen, angle, x, y, ponto_b):
        super().__init__(screen, angle, x, y)
        self.ponto_a = (x, y)
        self.ponto_b = ponto_b if ponto_b else (x + 100, y)
        self.alvo_patrulha_atual = self.ponto_b
    
    def update(self, player, delta_time, enemy_shots_group, walls_group):
        if self.estado == ESTADO_PATRULHA:
            self.patrulhar()
        # Chama o update da classe Inimigo para lidar com os outros estados e movimento
        super().update(player, delta_time, enemy_shots_group, walls_group)

    def patrulhar(self):
        if self.definir_movimento_para_alvo(self.alvo_patrulha_atual):
            self.alvo_patrulha_atual = self.ponto_a if self.alvo_patrulha_atual == self.ponto_b else self.ponto_b
    
    def retornar(self):
        dist_a = math.hypot(self.rect.centerx - self.ponto_a[0], self.rect.centery - self.ponto_a[1])
        dist_b = math.hypot(self.rect.centerx - self.ponto_b[0], self.rect.centery - self.ponto_b[1])
        ponto_retorno = self.ponto_a if dist_a < dist_b else self.ponto_b
        self.alvo_patrulha_atual = ponto_retorno
        if self.definir_movimento_para_alvo(ponto_retorno):
            self.estado = ESTADO_PATRULHA

class Inimigo_Melee(Inimigo):
    def __init__(self, screen, angle, x, y):
        super().__init__(screen, "jogo/sprites/inimigo_semarma.png", angle, x, y)
        self.velocidade_corrida = 180
        self.alcance_ataque = 60
        self.dano = 1
        self.cooldown_ataque = 1.2
        self.tempo_ultimo_ataque = 0

    def update(self, player, delta_time, enemy_shots_group, walls_group):
        if self.estado == ESTADO_PATRULHA:
            self.vx, self.vy = 0, 0 # Melee fica parado
        super().update(player, delta_time, enemy_shots_group, walls_group)

    def atirar(self, enemy_shots_group): pass
    def recarregar(self, delta_time): pass

    def atacar(self, player, delta_time, enemy_shots_group, walls_group):
        if not self.pode_ver_alvo(player, walls_group):
            self.estado = ESTADO_BUSCA
            return
        
        self.definir_movimento_para_alvo(player.rect.center)
        dist_jogador = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)
        
        tempo_atual = pygame.time.get_ticks() / 1000
        if dist_jogador <= self.alcance_ataque:
            if tempo_atual - self.tempo_ultimo_ataque > self.cooldown_ataque:
                player.sofrer_dano(self.dano)
                self.tempo_ultimo_ataque = tempo_atual