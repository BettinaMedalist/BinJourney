import pygame
import math
import random
from constantes import *
from classes.inimigo import *
from classes.parede import Parede
from classes.health_drop import HealthDrop
from classes.caixaarma import CaixaArma
from classes.upgrade import Upgrade
from classes.tile import Tile


class Fase:

    def __init__(self, screen, player, delta_time):
        self.screen = screen
        self.delta_time = delta_time
        self.player = player

        self.background_group = pygame.sprite.Group()  # Apenas tiles visuais do cenário
        self.walls = pygame.sprite.Group()            # Apenas paredes de colisão invisíveis
        self.main_sprites = pygame.sprite.Group()     # Sprites ativos e visíveis (inimigos, caixas, etc)
        self.enemies = pygame.sprite.Group()
        self.enemy_shots = pygame.sprite.Group()
        self.drops = pygame.sprite.Group()
        self.weapon_boxes = pygame.sprite.Group()
        self.upgrades = pygame.sprite.Group()

        # Lista de grupos que devem se mover com a câmera
        self.world_groups = [self.background_group, self.walls, self.main_sprites, self.enemy_shots]

    def add_enemy(self, enemy_type, angle, x, y, ponto_b=None):
        """Cria um inimigo e o adiciona aos grupos corretos."""
        new_enemy = None
        if enemy_type == "pistola":
            new_enemy = Inimigo_Pistola(self.screen, angle, x, y)
        elif enemy_type == "metralhadora":
            new_enemy = Inimigo_Metralhadora(self.screen, angle, x, y)
        elif enemy_type == "pistola_patrulha":
            new_enemy = Inimigo_Pistola_Patrulha(self.screen, angle, x, y, ponto_b)
        elif enemy_type == "melee":
            new_enemy = Inimigo_Melee(self.screen, angle, x, y)

        if new_enemy:
            self.enemies.add(new_enemy)
            self.main_sprites.add(new_enemy)

    def add_object(self, object_type, angle, x, y):
        """Cria paredes de colisão ou upgrades."""
        if object_type == "parede":
            self.walls.add(Parede(x, y))
        elif object_type == "upgrade":
            new_upgrade = Upgrade(self.screen, x, y)
            self.upgrades.add(new_upgrade)
            self.main_sprites.add(new_upgrade)

    def add_caixa_arma(self, x, y, tipo_arma):
        """Cria uma caixa de arma."""
        new_box = CaixaArma(self.screen, x, y, tipo_arma)
        self.weapon_boxes.add(new_box)
        self.main_sprites.add(new_box)

    # --- MÉTODOS DE LÓGICA PRINCIPAL ---
    def update(self, delta_time):
        self.delta_time = delta_time
        self.enemies.update(self.player, self.delta_time, self.enemy_shots, self.walls)
        self.drops.update()
        self.enemy_shots.update(self.delta_time)
        self.checar_alertas()
        self.checar_colisoes()
        self.movement()

    def movement(self):
        if self.player.direction.length() == 0:
            return
            
        self.player.direction.normalize_ip()
        mov_x = self.player.direction.x * self.player.speed * self.delta_time
        hitbox_copy = self.player.hitbox.copy()
        hitbox_copy.x += mov_x
        
        if hitbox_copy.collidelist([wall.rect for wall in self.walls]) == -1:
            for group in self.world_groups:
                for sprite in group:
                    sprite.rect.x -= mov_x
            for shot in self.player.shots:
                shot.rect.x -= mov_x

        mov_y = self.player.direction.y * self.player.speed * self.delta_time
        hitbox_copy = self.player.hitbox.copy()
        hitbox_copy.y += mov_y

        if hitbox_copy.collidelist([wall.rect for wall in self.walls]) == -1:
            # Move todas as camadas do mundo se não houver colisão
            for group in self.world_groups:
                for sprite in group:
                    sprite.rect.y -= mov_y
            for shot in self.player.shots:
                shot.rect.y -= mov_y

    def checar_colisoes(self):

        hits = pygame.sprite.groupcollide(self.player.shots, self.enemies, False, False)
        for shot, hit_enemies in hits.items():
            for enemy in hit_enemies:
                if enemy.hitbox.colliderect(shot.rect):
                    enemy.sofrer_dano(1)
                    shot.kill()
                    if enemy.vidas <= 0:
                        if random.random() < 0.25:
                            self.drops.add(HealthDrop(self.screen, enemy.rect.centerx, enemy.rect.centery))

        pygame.sprite.groupcollide(self.player.shots, self.walls, True, False)
        pygame.sprite.groupcollide(self.enemy_shots, self.walls, True, False)


        if not self.player.is_invulnerable:
            collided_shots = pygame.sprite.spritecollide(self.player, self.enemy_shots, True)
            for shot in collided_shots:
                if self.player.hitbox.colliderect(shot.rect):
                    self.player.sofrer_dano(1)
                    break


    def checar_alertas(self):
        for inimigo in self.enemies:
            if inimigo.estado in [ESTADO_PATRULHA, ESTADO_RETORNO, ESTADO_BUSCA]:
                if inimigo.pode_ver_alvo(self.player, self.walls):
                    inimigo.estado = ESTADO_ATAQUE

    def render(self):

        self.background_group.draw(self.screen)

        self.main_sprites.draw(self.screen)
        if self.player.visible:
            self.screen.blit(self.player.image, self.player.rect)
        self.player.shots.draw(self.screen)
        self.enemy_shots.draw(self.screen)

        for inimigo in self.enemies:
            if hasattr(inimigo, 'icone_estado_atual') and inimigo.icone_estado_atual:
                icone_rect = inimigo.icone_estado_atual.get_rect(center=(inimigo.rect.centerx, inimigo.rect.top - 20))
                self.screen.blit(inimigo.icone_estado_atual, icone_rect)