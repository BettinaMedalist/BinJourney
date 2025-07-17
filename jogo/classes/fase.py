from classes.health_drop import*
from classes.inimigo import*
from classes.upgrade import*
from classes.caixaarma import*
from classes.tile import*
from constantes import*
import math
import random
import pygame

RAIO_SOM_METRALHADORA = 400
RAIO_SOM_CORRIDA = 200


class Fase:
    def __init__(self, screen, player):
        # As listas foram substituídas por Grupos de Sprites
        self.screen = screen
        self.player = player

        self.visible_sprites = pygame.sprite.LayeredUpdates()
        self.obstacles_sprites = pygame.sprite.Group()

        self.enemies = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()
        self.drops = pygame.sprite.Group()
        self.caixa_de_armas = pygame.sprite.Group()

        self.visible_sprites.add(self.player)

    def create_level(self, layout, tile_size):
        chao_tile_img = pygame.image.load("jogo/sprites/chaoconcreto.png").convert_alpha()
        parede_tile_img = pygame.image.load("jogo/sprites/paredetuto.png").convert_alpha()

        for row_index, row in enumerate(layout):
            for col_index, tile_code in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                # Lógica para o chão (desenhado sob todos os objetos)
                if tile_code != 'W':
                    Tile(chao_tile_img, x, y, groups=[self.visible_sprites], layer=CAMADA_CHAO)

                # Lógica para os objetos específicos
                if tile_code == 'W': # Parede
                    Tile(parede_tile_img, x, y, groups=[self.visible_sprites, self.obstacles_sprites], layer=CAMADA_PAREDE)

                elif tile_code == 'J':  # Jogador
                    self.player.rect.topleft = (x, y)

                elif tile_code == 'G':  # Inimigo com Pistola
                    self.add_enemy("pistola", 0, x, y)

    def add_enemy(self, enemy_type, angle, x, y, ponto_b=None):
        # Adiciona inimigos ao grupo .enemies
        inimigo = None
        if enemy_type == "pistola":
            inimigo = (Inimigo_Pistola(self.screen, angle, x, y))
        elif enemy_type == "metralhadora":
            inimigo = (Inimigo_Metralhadora(self.screen, angle, x, y))
        elif enemy_type == "pistola_patrulha":
            inimigo = (Inimigo_Pistola_Patrulha(self.screen, angle, x, y, ponto_b))
        elif enemy_type == "melee":
            inimigo = (Inimigo_Melee(self.screen, angle, x, y))
        
        if inimigo:
            inimigo._layer = CAMADA_INIMIGO
            self.visible_sprites.add(inimigo)
            self.enemies.add(inimigo)
            
    def add_object(self, object_type, angle, x, y):
        # Adiciona objetos ao grupo .objects
        objeto = None
        if object_type == "parede":
            pass
        elif object_type == "upgrade":
            objeto = (Upgrade(self.screen, x, y))
        if objeto:
            self.visible_sprites.add(objeto)  
            self.objects.add(objeto)      

    def add_caixa_arma(self, x, y, tipo_arma):
        # Adiciona caixas ao grupo .caixa_de_armas
        
        caixa = (CaixaArma(self.screen, x, y, tipo_arma))
        self.caixa_de_armas.add(caixa)
        self.visible_sprites.add(caixa)

    
    def update(self, delta_time):
        camera_move_x = (self.player.left - self.player.right) * delta_time * self.player.running
        camera_move_y = (self.player.up - self.player.down) * delta_time * self.player.running
        
        for sprite in self.visible_sprites:
            if sprite != self.player:
                sprite.rect.x += camera_move_x
                sprite.rect.y += camera_move_y
        
        # Lógica de colisão com upgrades
        if pygame.sprite.spritecollide(self.player, self.obstacles_sprites, False, pygame.sprite.collide_rect_ratio(0.75)):
            # 3. Se colidiu, desfaz o movimento de TODOS os sprites para impedir que a câmera avance
            for sprite in self.visible_sprites:
                if sprite != self.player:
                    sprite.rect.x -= camera_move_x
                    sprite.rect.y -= camera_move_y

        collided_upgrades = pygame.sprite.spritecollide(self.player, self.objects, True, pygame.sprite.collide_rect_ratio(0.75))
        for upgrade in collided_upgrades:
            if isinstance(upgrade, Upgrade):
                self.player.max_vidas += 1
                self.player.vidas = self.player.max_vidas

        # Lógica de colisão com caixas de armas
        collided_caixas = pygame.sprite.spritecollide(self.player, self.caixa_de_armas, False, pygame.sprite.collide_rect_ratio(0.75))
        for caixa in collided_caixas:
            if not caixa.usada:
                caixa.abrir()
                self.player.armas_desbloqueadas.add(caixa.tipo_arma)
                self.player.arma = caixa.tipo_arma
                print(f"Arma adquirida por toque: {caixa.tipo_arma}")
        
        # Atualiza inimigos e seus tiros
        for inimigo in self.enemies:
            if hasattr(inimigo, 'ponto_a'):
                inimigo.ponto_a = (inimigo.ponto_a[0] + camera_move_x, inimigo.ponto_a[1] + camera_move_y)
                inimigo.ponto_b = (inimigo.ponto_b[0] + camera_move_x, inimigo.ponto_b[1] + camera_move_y)
                inimigo.alvo_patrulha_atual = (inimigo.alvo_patrulha_atual[0] + camera_move_x, inimigo.alvo_patrulha_atual[1] + camera_move_y)
            if inimigo.alvo_busca:
                inimigo.alvo_busca[0] += camera_move_x
                inimigo.alvo_busca[1] += camera_move_y

            inimigo.rect.x += (inimigo.vx * delta_time)
            inimigo.rect.y += (inimigo.vy * delta_time)
            inimigo.px += camera_move_x
            inimigo.py += camera_move_y

            for bala in inimigo.shots:
                bala.rect.x += camera_move_x
                bala.rect.y += camera_move_y
            
            inimigo.shots.update(delta_time)
            for bala in inimigo.shots:
                if not self.screen.get_rect().colliderect(bala.rect):
                    bala.kill() # Remove a bala do grupo se sair da tela
        
        # Atualiza os inimigos
        self.enemies.update(self.player, delta_time)
        self.caixa_de_armas.update() # Assumindo que CaixaArma tenha um método update
        
        # Lógica de drops
        for drop in self.drops:
            if pygame.time.get_ticks() - drop.creation_time > drop.lifetime:
                drop.kill() # Remove o drop se o tempo de vida expirar
                continue
        
        collided_drops = pygame.sprite.spritecollide(self.player, self.drops, True, pygame.sprite.collide_rect_ratio(0.75))
        for drop in collided_drops:
            if self.player.vidas < self.player.max_vidas:
                self.player.vidas += 1

        self.checar_alertas()
        self.checar_colisoes()

    def checar_alertas(self):
        for inimigo in self.enemies:
            if inimigo.estado in [ESTADO_PATRULHA, ESTADO_RETORNO, ESTADO_BUSCA]:
                if inimigo.pode_ver_alvo(self.player):
                    inimigo.estado = ESTADO_ATAQUE
        
        if self.player.shooting and self.player.arma == METRALHADORA:
            self.propagar_som(self.player.rect.center, RAIO_SOM_METRALHADORA)
            
        if self.player.running > 1:
            self.propagar_som(self.player.rect.center, RAIO_SOM_CORRIDA)

    def propagar_som(self, origem, raio):
        for inimigo in self.enemies:
            if inimigo.estado == ESTADO_PATRULHA:
                dist = math.hypot(inimigo.rect.centerx - origem[0], inimigo.rect.centery - origem[1])
                if dist <= raio:
                    inimigo.alvo_busca = list(origem)
                    inimigo.estado = ESTADO_BUSCA

    def checar_colisoes(self):
        # Colisão entre tiros do jogador e inimigos
        # groupcollide retorna um dicionário {inimigo: [balas]}
        colisoes_inimigos = pygame.sprite.groupcollide(self.enemies, self.player.shots, False, True)
        for inimigo_atingido, balas_colididas in colisoes_inimigos.items():
            era_furtivo = self.player.running == 1 and (inimigo_atingido.estado in [ESTADO_PATRULHA, ESTADO_RETORNO])

            if era_furtivo:
                inimigo_atingido.vidas = 0
            else:
                inimigo_atingido.vidas -= 1
            
            if inimigo_atingido.vidas <= 0:
                if random.random() < 0.25:
                    novo_drop = HealthDrop(self.screen, inimigo_atingido.rect.centerx, inimigo_atingido.rect.centery)
                    self.drops.add(novo_drop)
                    print(f"--> DROP CRIADO: ID={id(novo_drop)}, Pos={inimigo_atingido.rect.center}")

                if era_furtivo:
                    for outro_inimigo in self.enemies:
                        if outro_inimigo is not inimigo_atingido and outro_inimigo.pode_ver_alvo(inimigo_atingido):
                            outro_inimigo.estado = ESTADO_BUSCA
                            outro_inimigo.alvo_busca = list(inimigo_atingido.rect.center)
                else:
                    self.propagar_som(inimigo_atingido.rect.center, RAIO_SOM_METRALHADORA)
                
                inimigo_atingido.kill() # Remove o inimigo de todos os grupos
            else:
                self.propagar_som(inimigo_atingido.rect.center, RAIO_SOM_METRALHADORA)

        # Colisão entre tiros inimigos e jogador
        for inimigo in self.enemies:
            colisoes_jogador = pygame.sprite.spritecollide(self.player, inimigo.shots, True)
            if colisoes_jogador:
                if not self.player.is_invulnerable:
                    self.player.sofrer_dano(len(colisoes_jogador)) # Causa dano por cada bala
                    if self.player.vidas <= 0:
                        print("GAME OVER")

    def render(self):
        self.visible_sprites.draw(self.screen)
        
        # Usa o método .draw() dos grupos para renderizar todos os sprites de uma vez
        for inimigo in self.enemies:
            inimigo.draw_vision_cone()
            inimigo.shots.draw(self.screen) # Desenha todos os tiros do inimigo
            if inimigo.icone_estado_atual:
                icone_rect = inimigo.icone_estado_atual.get_rect(center=(inimigo.rect.centerx, inimigo.rect.top - 20))
                self.screen.blit(inimigo.icone_estado_atual, icone_rect)