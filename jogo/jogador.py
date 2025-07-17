# Arquivo: jogador.py (VERSÃO FINAL E CORRETA)

import pygame
from constantes import *
from classes.game_object import GameObject
from classes.tiro import Tiro
from utils.funcoes import carregar_imagem

class Player(GameObject):
    def __init__(self, screen):
        super().__init__(screen, "jogo/sprites/player_semarma.png")
        self.vidas = 3
        self.max_vidas = 3
        self.visible = True
        self.speed = 400
        self.running = 1
        self.up, self.down, self.left, self.right = 0, 0, 0, 0
        self.direction = pygame.math.Vector2()
        self.hitbox = self.rect.inflate(-50, -50)
        self.shooting = False
        self.armas_desbloqueadas = {MAO, PISTOLA}
        self.arma = PISTOLA
        self.m_pistola, self.m_metralhadora, self.cadence_metralhadora = 10, 30, 0
        self.sprites = {
            "mao": carregar_imagem("jogo/sprites/player_semarma.png"),
            "pistola": carregar_imagem("jogo/sprites/player_pistola.png"),
            "metralhadora": carregar_imagem("jogo/sprites/player_metralhadora.png")
        }
        self.shots = pygame.sprite.Group()
        self.original_image = self.sprites["pistola"]
        self.is_invulnerable = False
        self.invulnerability_duration = 2
        self.invulnerability_end_time = 0
        self.blink_timer, self.blink_rate = 0, 0.1

    def update(self, delta_time):

        mov_x = self.right - self.left
        mov_y = self.down - self.up
        self.direction = pygame.math.Vector2(mov_x, mov_y)

        if self.is_invulnerable:
            current_time = pygame.time.get_ticks() / 1000
            self.blink_timer += delta_time
            if self.blink_timer >= self.blink_rate:
                self.visible = not self.visible
                self.blink_timer = 0
            if current_time >= self.invulnerability_end_time:
                self.is_invulnerable, self.visible = False, True

        self.hitbox.center = self.rect.center

        self.aim()
        self.shoot(delta_time)

    def aim(self):
        centro_antigo = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=centro_antigo)
    
    def shoot(self, delta_time):
        self.cadence_metralhadora += delta_time
        if not self.shooting: return
        tiro_criado = None
        if self.arma == PISTOLA and self.m_pistola > 0:
            tiro_criado = Tiro(self.screen, self)
            self.m_pistola -= 1
            self.shooting = False
        elif self.arma == METRALHADORA and self.m_metralhadora > 0 and self.cadence_metralhadora >= 0.15:
            tiro_criado = Tiro(self.screen, self)
            self.m_metralhadora -= 1
            self.cadence_metralhadora = 0
        if tiro_criado:
            self.shots.add(tiro_criado)

    def trade_weapons(self, nova_arma):
        if self.arma == nova_arma: return
        self.arma = nova_arma
        centro_antigo = self.rect.center
        if self.arma in self.sprites:
            self.original_image = self.sprites.get(self.arma)
        self.rect = self.original_image.get_rect(center=centro_antigo)

    def sofrer_dano(self, quantidade):
        if self.is_invulnerable: return False
        self.vidas -= quantidade
        self.is_invulnerable = True
        self.invulnerability_end_time = (pygame.time.get_ticks() / 1000) + self.invulnerability_duration
        if self.vidas <= 0: self.vidas = 0
        return True

    def respawn(self):
        self.vidas = self.max_vidas
        self.is_invulnerable, self.visible = False, True