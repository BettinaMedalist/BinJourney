from classes.health_drop import*
from classes.inimigo import*
from classes.upgrade import*
from classes.caixaarma import*
from constantes import*
import math
import random
import pygame

RAIO_SOM_METRALHADORA = 400
RAIO_SOM_CORRIDA = 200

class Fase(GameObject):
    def __init__(self, screen, image_path, player):
        super().__init__(screen, image_path)
        # As listas foram substituídas por Grupos de Sprites
        self.enemies = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()
        self.drops = pygame.sprite.Group()
        self.caixa_de_armas = pygame.sprite.Group()

        self.player = player

    def add_enemy(self, enemy_type, angle, x, y, ponto_b=None):
        # Adiciona inimigos ao grupo .enemies
        if enemy_type == "pistola":
            self.enemies.add(Inimigo_Pistola(self.screen, angle, x, y))
        elif enemy_type == "metralhadora":
            self.enemies.add(Inimigo_Metralhadora(self.screen, angle, x, y))
        elif enemy_type == "pistola_patrulha":
            self.enemies.add(Inimigo_Pistola_Patrulha(self.screen, angle, x, y, ponto_b))
        elif enemy_type == "melee":
            self.enemies.add(Inimigo_Melee(self.screen, angle, x, y))
            
    def add_object(self, object_type, angle, x, y):
        # Adiciona objetos ao grupo .objects
        if object_type == "parede":
            pass
        elif object_type == "upgrade":
            self.objects.add(Upgrade(self.screen, x, y))

    def add_caixa_arma(self, x, y, tipo_arma):
        # Adiciona caixas ao grupo .caixa_de_armas
        self.caixa_de_armas.add(CaixaArma(self.screen, x, y, tipo_arma))

    
    def update(self, delta_time):
        camera_move_x = (self.player.left - self.player.right) * delta_time * self.player.running
        camera_move_y = (self.player.up - self.player.down) * delta_time * self.player.running
        
        self.rect.x += camera_move_x
        self.rect.y += camera_move_y

        # Atualiza a posição de todos os sprites nos grupos com base na câmera
        for group in [self.objects, self.player.shots, self.caixa_de_armas, self.drops]:
            for sprite in group:
                sprite.rect.x += camera_move_x
                sprite.rect.y += camera_move_y
        
        # Lógica de colisão com upgrades
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

            inimigo.rect.x += camera_move_x + (inimigo.vx * delta_time)
            inimigo.rect.y += camera_move_y + (inimigo.vy * delta_time)
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
        self.draw()
        
        # Usa o método .draw() dos grupos para renderizar todos os sprites de uma vez
        self.objects.draw(self.screen)
        self.caixa_de_armas.draw(self.screen)
        self.drops.draw(self.screen)
        
        for inimigo in self.enemies:
            inimigo.draw() # Desenha o inimigo individualmente
            inimigo.draw_vision_cone()
            inimigo.shots.draw(self.screen) # Desenha todos os tiros do inimigo
            if inimigo.icone_estado_atual:
                icone_rect = inimigo.icone_estado_atual.get_rect(center=(inimigo.rect.centerx, inimigo.rect.top - 20))
                self.screen.blit(inimigo.icone_estado_atual, icone_rect)