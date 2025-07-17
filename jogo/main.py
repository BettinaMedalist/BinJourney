import pygame
from constantes import *
from jogador import Player
from menu import MenuPrincipal, MenuPause
from hud import Hud
from fases.tutorial import Tutorial
from fases.fase1 import Fase1


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Bin Journey")
        self.screen = pygame.display.set_mode((16 * RES, 9 * RES))
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        self.game_state = MENU
        self.running = True

        self.hud = Hud(self.screen)
        self.player = Player(self.screen)
        self.player.rect.center = self.screen.get_rect().center
        self.fase_atual_tipo = Tutorial
        self.fase = self.fase_atual_tipo(self.screen, self.player, self.delta_time)
        self.menu_principal = MenuPrincipal(self.screen)
        self.menu_pause = MenuPause(self.screen)

    def handle_events(self):
        self.delta_time = self.clock.tick(FPS) / 1000
        self.events = pygame.event.get()

        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == RODANDO:
                        self.game_state = PAUSADO
                    elif self.game_state == PAUSADO:
                        self.game_state = RODANDO

                if event.key == pygame.K_1:
                    if MAO in self.player.armas_desbloqueadas: self.player.trade_weapons(MAO)
                elif event.key == pygame.K_2:
                    if PISTOLA in self.player.armas_desbloqueadas: self.player.trade_weapons(PISTOLA)
                elif event.key == pygame.K_3:
                    if METRALHADORA in self.player.armas_desbloqueadas: self.player.trade_weapons(METRALHADORA)

                if event.key == pygame.K_w: self.player.up = 1
                if event.key == pygame.K_a: self.player.left = 1
                if event.key == pygame.K_s: self.player.down = 1
                if event.key == pygame.K_d: self.player.right = 1

                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    self.player.shooting = True
                    if event.key == pygame.K_UP: self.player.angle = CIMA
                    if event.key == pygame.K_DOWN: self.player.angle = BAIXO
                    if event.key == pygame.K_LEFT: self.player.angle = ESQUERDA
                    if event.key == pygame.K_RIGHT: self.player.angle = DIREITA

                if event.key == pygame.K_LSHIFT: self.player.running = 3
                if event.key == pygame.K_r: self.player.recarregar()  # Supondo um método recarregar

            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    self.player.shooting = False
                if event.key == pygame.K_w: self.player.up = 0
                if event.key == pygame.K_s: self.player.down = 0
                if event.key == pygame.K_a: self.player.left = 0
                if event.key == pygame.K_d: self.player.right = 0
                if event.key == pygame.K_LSHIFT: self.player.running = 1

    def render(self):
        self.screen.fill((20, 20, 20))  # Um fundo escuro padrão

        if self.game_state == MENU:
            self.game_state = self.menu_principal.executar(self.game_state, self.events)

        elif self.game_state == RODANDO:
            self.fase.render()  # Nosso render limpo
            self.hud.mostrar_vida(self.player)
            self.hud.mostrar_arma(self.player)

        elif self.game_state == PAUSADO:
            self.fase.render()
            self.game_state = self.menu_pause.executar(self.game_state, self.events)

        elif self.game_state == SAIR:
            self.running = False

        pygame.display.flip()

    def update(self):
        if self.player.vidas <= 0:
            self.game_state = MORTO

        if self.game_state == MORTO:
            self.fase = self.fase_atual_tipo(self.screen, self.player, self.delta_time)
            self.player.respawn()
            self.game_state = RODANDO
            return
        
        if self.game_state == RODANDO:
            self.player.update(self.delta_time)
            self.player.shots.update(self.delta_time)
            self.fase.update(self.delta_time)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()

        pygame.quit()


if __name__ == '__main__':
    Game().run()