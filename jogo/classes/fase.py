import pygame
import math
import random
from constantes import *

# Importe as classes de objetos que a fase vai criar
from classes.inimigo import Inimigo_Pistola, Inimigo_Metralhadora, Inimigo_Pistola_Patrulha, Inimigo_Melee
from classes.parede import Parede
from classes.health_drop import HealthDrop
from classes.caixaarma import CaixaArma
from classes.upgrade import Upgrade
from classes.tile import Tile


class Fase:
    def __init__(self, screen, player, delta_time):
        """
        Prepara a fase criando todos os grupos de sprites necessários.
        Estes grupos funcionarão como "camadas" e "categorias" para gerenciar
        todos os objetos do jogo de forma eficiente.
        """
        self.screen = screen
        self.delta_time = delta_time
        self.player = player

        # --- GRUPOS DE SPRITES ---
        # Grupos de renderização e lógica
        self.background_group = pygame.sprite.Group() # Tiles visuais do cenário
        self.main_sprites = pygame.sprite.Group()     # Sprites ativos (inimigos, caixas, drops)

        # Grupos específicos para colisões e lógica
        self.walls = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemy_shots = pygame.sprite.Group()
        self.drops = pygame.sprite.Group()
        self.weapon_boxes = pygame.sprite.Group()
        self.upgrades = pygame.sprite.Group()

        # Lista de grupos que se movem com a câmera
        self.world_groups = [self.background_group, self.walls, self.enemies,
                             self.enemy_shots, self.drops, self.weapon_boxes, self.upgrades]

    def add_enemy(self, enemy_type, angle, x, y, ponto_b=None):
        """Cria um inimigo do tipo especificado e o adiciona aos grupos corretos."""
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
        """Cria um objeto (parede de colisão, upgrade) e o adiciona aos grupos."""
        if object_type == "parede":
            new_wall = Parede(x, y)
            self.walls.add(new_wall)
        elif object_type == "upgrade":
            new_upgrade = Upgrade(self.screen, x, y)
            self.upgrades.add(new_upgrade)
            self.main_sprites.add(new_upgrade)

    def add_caixa_arma(self, x, y, tipo_arma):
        """Cria uma caixa de arma e a adiciona aos grupos."""
        new_box = CaixaArma(self.screen, x, y, tipo_arma)
        self.weapon_boxes.add(new_box)
        self.main_sprites.add(new_box)

    def update(self):
        """
        O "coração" da fase. Orquestra todas as atualizações de lógica,
        movimento, IA e colisões a cada frame.
        """
        # 1. ATUALIZAÇÃO DE ESTADO DOS OBJETOS
        # Chama o método .update() de cada sprite em seus respectivos grupos
        self.player.update(self.walls, self.delta_time, self.main_sprites) # O update do jogador precisa dos grupos
        self.player.shots.update(self.delta_time)
        self.enemies.update(self.player, self.delta_time, self.enemy_shots, self.walls)
        self.enemy_shots.update(self.delta_time)
        self.drops.update()

        # 2. MOVIMENTO DA CÂMERA (COM COLISÃO)
        self.movement()

        # 3. LÓGICA DE IA
        self.checar_alertas()

        # 4. LÓGICA DE COLISÕES
        self.checar_colisoes()

    def movement(self):
        """Move o mundo ao redor do jogador e lida com a colisão do jogador com as paredes."""
        if self.player.direction.length() > 0:
            self.player.direction.normalize_ip()

        # --- Eixo Horizontal ---
        mov_x = self.player.direction.x * self.player.speed * self.delta_time
        player_rect_copy = self.player.rect.copy()
        player_rect_copy.x += mov_x

        if not pygame.sprite.spritecollide(player_rect_copy, self.walls, False):
            for group in self.world_groups:
                for sprite in group:
                    sprite.rect.x -= mov_x

        # --- Eixo Vertical ---
        mov_y = self.player.direction.y * self.player.speed * self.delta_time
        player_rect_copy = self.player.rect.copy()
        player_rect_copy.y += mov_y

        if not pygame.sprite.spritecollide(player_rect_copy, self.walls, False):
            for group in self.world_groups:
                for sprite in group:
                    sprite.rect.y -= mov_y

    def checar_alertas(self):
        """Verifica a IA dos inimigos, se eles veem o jogador ou ouvem sons."""
        for inimigo in self.enemies:
            if inimigo.estado in [ESTADO_PATRULHA, ESTADO_RETORNO, ESTADO_BUSCA]:
                if inimigo.pode_ver_alvo(self.player, self.walls):
                    inimigo.estado = ESTADO_ATAQUE

        if self.player.shooting and self.player.arma == METRALHADORA:
            self.propagar_som(self.player.rect.center, RAIO_SOM_METRALHADORA)
        if self.player.running > 1:
            self.propagar_som(self.player.rect.center, RAIO_SOM_CORRIDA)

    def propagar_som(self, origem, raio):
        """Avisa inimigos próximos sobre um som."""
        for inimigo in self.enemies:
            if inimigo.estado == ESTADO_PATRULHA:
                dist = math.hypot(inimigo.rect.centerx - origem[0], inimigo.rect.centery - origem[1])
                if dist <= raio:
                    inimigo.alvo_busca = list(origem)
                    inimigo.estado = ESTADO_BUSCA

    def checar_colisoes(self):
        """Verifica todas as interações de colisão usando as funções do Pygame."""
        # Tiros do Player vs Inimigos
        hits = pygame.sprite.groupcollide(self.player.shots, self.enemies, True, False)
        for bala, inimigos_atingidos in hits.items():
            for inimigo in inimigos_atingidos:
                inimigo.sofrer_dano(1) # Supondo um método para dano
                # Se o inimigo morrer, ele pode dropar um item
                if inimigo.vidas <= 0:
                    if random.random() < 0.25: # 25% de chance de drop
                        self.drops.add(HealthDrop(self.screen, inimigo.rect.centerx, inimigo.rect.centery))

        # Tiros (Player e Inimigo) vs Paredes
        pygame.sprite.groupcollide(self.player.shots, self.walls, True, False)
        pygame.sprite.groupcollide(self.enemy_shots, self.walls, True, False)

        # Tiros dos Inimigos vs Player
        if not self.player.is_invulnerable:
            player_hit = pygame.sprite.spritecollide(self.player, self.enemy_shots, True)
            if player_hit:
                self.player.sofrer_dano(1)

        # Player vs Itens
        pygame.sprite.spritecollide(self.player, self.drops, True, pygame.sprite.collide_mask) # Coleta drops
        pygame.sprite.spritecollide(self.player, self.upgrades, True) # Coleta upgrades
        caixas_abertas = pygame.sprite.spritecollide(self.player, self.weapon_boxes, False)
        for caixa in caixas_abertas:
            caixa.abrir() # Lógica de abrir a caixa fica na própria caixa

    def render(self):
        """Desenha todas as camadas do jogo na ordem correta."""
        self.background_group.draw(self.screen)
        self.drops.draw(self.screen)
        self.weapon_boxes.draw(self.screen)
        self.upgrades.draw(self.screen)
        self.main_sprites.draw(self.screen) # Desenha inimigos
        self.screen.blit(self.player.image, self.player.rect) # Desenha o jogador
        self.player.shots.draw(self.screen)
        self.enemy_shots.draw(self.screen)

        # Lógica de desenho de overlays (ícones, etc)
        for inimigo in self.enemies:
            if hasattr(inimigo, 'icone_estado_atual') and inimigo.icone_estado_atual:
                icone_rect = inimigo.icone_estado_atual.get_rect(center=(inimigo.rect.centerx, inimigo.rect.top - 20))
                self.screen.blit(inimigo.icone_estado_atual, icone_rect)