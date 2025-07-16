# Arquivo: classes/fase.py (Substitua o conteúdo)
from classes.health_drop import*
from classes.inimigo import*
from classes.parede import*
from constantes import*
import math
import random
import pygame

RAIO_SOM_METRALHADORA = 400
RAIO_SOM_CORRIDA = 200

class Fase(GameObject):
    def __init__(self, screen, image_path, player):
        super().__init__(screen, image_path)
        #Lista de inimigos na fase
        self.enemies = []
        #Lista de paredes e obstaculos
        self.objects = []

        self.drops = []

        self.player = player


    def add_enemy(self, enemy_type, angle, x, y, ponto_b=None):
        if enemy_type == "pistola":
            self.enemies.append(Inimigo_Pistola(self.screen, angle, x, y))
        elif enemy_type == "metralhadora":
            self.enemies.append(Inimigo_Metralhadora(self.screen, angle, x, y))
        elif enemy_type == "pistola_patrulha":
            self.enemies.append(Inimigo_Pistola_Patrulha(self.screen, angle, x, y, ponto_b))
        # SUBSTITUA "melee" por "melee_patrulha"
        elif enemy_type == "melee":
            self.enemies.append(Inimigo_Melee(self.screen, angle, x, y))
            
    def add_object(self, object_type, angle, x, y):
        if object_type == "parede":
            self.objects.append(Parede(self.screen, x, y))
    
    def update(self, delta_time):
        #Movimentação que vai afetar a todas as entidades para fazer o player andar
        camera_move_x = (self.player.left - self.player.right) * delta_time * self.player.running
        camera_move_y = (self.player.up - self.player.down) * delta_time * self.player.running
        
        #Faz o fundo andar
        self.rect.x += camera_move_x
        self.rect.y += camera_move_y

        #Faz os objetos andarem
        for objeto in self.objects:
            objeto.rect.x += camera_move_x
            objeto.rect.y += camera_move_y
        
        #Impedem que as balas andem junto com o player
        for bala in self.player.shots:
            bala.rect.x += camera_move_x
            bala.rect.y += camera_move_y
        
        for inimigo in self.enemies:
            if hasattr(inimigo, 'ponto_a'):
                inimigo.ponto_a = (inimigo.ponto_a[0] + camera_move_x, inimigo.ponto_a[1] + camera_move_y)
                inimigo.ponto_b = (inimigo.ponto_b[0] + camera_move_x, inimigo.ponto_b[1] + camera_move_y)
                inimigo.alvo_patrulha_atual = (inimigo.alvo_patrulha_atual[0] + camera_move_x, inimigo.alvo_patrulha_atual[1] + camera_move_y)

            if inimigo.alvo_busca:
                inimigo.alvo_busca[0] += camera_move_x
                inimigo.alvo_busca[1] += camera_move_y

            inimigo.update(self.player, delta_time)

            inimigo.rect.x += camera_move_x + (inimigo.vx * delta_time)
            inimigo.rect.y += camera_move_y + (inimigo.vy * delta_time)

            inimigo.px += camera_move_x
            inimigo.py += camera_move_y

            for bala in inimigo.shots:
                bala.rect.x += camera_move_x
                bala.rect.y += camera_move_y
            for bala in inimigo.shots[:]:
                bala.update(delta_time)
                if not self.screen.get_rect().colliderect(bala.rect):
                    inimigo.shots.remove(bala)

        for drop in self.drops[:]:
            drop.rect.x += camera_move_x
            drop.rect.y += camera_move_y

            drop.hitbox.center = drop.rect.center

            if pygame.time.get_ticks() - drop.creation_time > drop.lifetime:
                self.drops.remove(drop)
                continue
                    
            if self.player.rect.colliderect(drop.rect):
                if self.player.vidas < self.player.max_vidas:
                    self.player.vidas += 1
                    self.drops.remove(drop)

        self.checar_alertas()
        self.checar_colisoes()

    def checar_alertas(self):
        for inimigo in self.enemies:
            if inimigo.estado == ESTADO_PATRULHA or inimigo.estado == ESTADO_RETORNO or inimigo.estado == ESTADO_BUSCA:
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
        for bala in self.player.shots[:]:
            for inimigo_atingido in self.enemies[:]:
                if inimigo_atingido.rect.colliderect(bala):
                    
                    era_furtivo = self.player.running == 1 and (inimigo_atingido.estado == ESTADO_PATRULHA or inimigo_atingido.estado == ESTADO_RETORNO)

                    if era_furtivo:
                        inimigo_atingido.vidas = 0
                    else:
                        inimigo_atingido.vidas -= 1

                    if bala in self.player.shots:
                        self.player.shots.remove(bala)
                    
                    if inimigo_atingido.vidas <= 0:
                        if random.random() < 0.25:
                            drop_x = inimigo_atingido.rect.centerx
                            drop_y = inimigo_atingido.rect.centery

                            novo_drop = HealthDrop(self.screen, drop_x, drop_y)
                            self.drops.append(novo_drop)
                            print(f"--> DROP CRIADO: ID={id(novo_drop)}, Pos=({drop_x}, {drop_y})")

                        if era_furtivo:
                            for outro_inimigo in self.enemies:
                                if outro_inimigo is not inimigo_atingido:
                                    if outro_inimigo.pode_ver_alvo(inimigo_atingido):
                                        outro_inimigo.estado = ESTADO_BUSCA
                                        outro_inimigo.alvo_busca = list(inimigo_atingido.rect.center)
                        else:
                            self.propagar_som(inimigo_atingido.rect.center, RAIO_SOM_METRALHADORA)
                        
                        self.enemies.remove(inimigo_atingido)
                    else:
                        self.propagar_som(inimigo_atingido.rect.center, RAIO_SOM_METRALHADORA)

                    break

        for inimigo in self.enemies:
            for bala in inimigo.shots[:]:
                if self.player.rect.colliderect(bala):
                    if not self.player.is_invulnerable:
                        self.player.sofrer_dano(1)
                        inimigo.shots.remove(bala)
                        if self.player.vidas <= 0:
                            print("GAME OVER")
                    else:
                        if bala in inimigo.shots:
                            inimigo.shots.remove(bala)
                    break


    def render(self):
        self.draw()
        for inimigo in self.enemies:
            inimigo.draw()
            inimigo.draw_vision_cone()
            for bala in inimigo.shots:
                bala.draw()
            if inimigo.icone_estado_atual:
                icone_rect = inimigo.icone_estado_atual.get_rect(center=(inimigo.rect.centerx, inimigo.rect.top - 20))
                self.screen.blit(inimigo.icone_estado_atual, icone_rect)

        for objeto in self.objects:
            objeto.draw()

        for drop in self.drops:
            drop.draw()
            #pygame.draw.rect(self.screen, (0, 255, 0), drop.rect, 2)