from constantes import*
from jogador import*
from menu import MenuPrincipal, MenuPause 
from hud import*
from fases.tutorial import*
from fases.fase1 import*

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
        self.player.shooting = False
        
        self.fase_atual_tipo = Tutorial
        self.fase = self.fase_atual_tipo(self.screen, self.player)
        self.levels = [Tutorial, Fase1]
        self.current_level_index = 0
        

        self.fase_atual_tipo = self.levels[self.current_level_index]
        self.fase = self.fase_atual_tipo(self.screen, self.player)

        self.menu_principal = MenuPrincipal(self.screen)
        self.menu_pause = MenuPause(self.screen)

    def handle_events(self):
        self.delta_time = self.clock.tick(FPS)/1000
        self.events = pygame.event.get()

        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = PAUSADO if self.game_state == RODANDO else RODANDO
                if event.key == pygame.K_1:
                    if MAO in self.player.armas_desbloqueadas: self.player.arma = MAO
                elif event.key == pygame.K_2:
                    if PISTOLA in self.player.armas_desbloqueadas: self.player.arma = PISTOLA
                elif event.key == pygame.K_3:
                    if METRALHADORA in self.player.armas_desbloqueadas: self.player.arma = METRALHADORA
                if event.key == pygame.K_RIGHT: self.player.angle = DIREITA; self.player.shooting = True
                elif event.key == pygame.K_UP: self.player.angle = CIMA; self.player.shooting = True
                elif event.key == pygame.K_LEFT: self.player.angle = ESQUERDA; self.player.shooting = True
                elif  event.key == pygame.K_DOWN: self.player.angle = BAIXO; self.player.shooting = True
                if event.key == pygame.K_w: self.player.up = self.player.speed
                if event.key == pygame.K_a: self.player.left = self.player.speed
                if event.key == pygame.K_s: self.player.down = self.player.speed
                if event.key == pygame.K_d: self.player.right = self.player.speed
                if event.key == pygame.K_LSHIFT: self.player.running = 3
                elif event.key == pygame.K_r:
                    if self.player.arma == PISTOLA: self.player.m_pistola = 10
                    elif self.player.arma == METRALHADORA: self.player.m_metralhadora = 30
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_RIGHT, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN]: self.player.shooting = False
                if event.key == pygame.K_w: self.player.up = 0
                if event.key == pygame.K_s: self.player.down = 0
                if event.key == pygame.K_a: self.player.left = 0
                if event.key == pygame.K_d: self.player.right = 0
                if event.key == pygame.K_LSHIFT: self.player.running = 1

    def render(self):
        self.screen.fill('yellow')
        if self.game_state == MENU:
            self.game_state = self.menu_principal.executar(self.game_state, self.events)
        elif self.game_state == RODANDO:
            if not self.fase.enemies:
                self.go_to_next_level()

            self.fase.render()
            self.player.draw()
            # Desenha todos os tiros do jogador de uma vez
            self.player.shots.draw(self.screen)
            self.hud.mostrar_vida(self.player)
            self.hud.mostrar_arma(self.player)

        elif self.game_state == PAUSADO:
            self.fase.render()
            self.player.shots.draw(self.screen)
            self.game_state = self.menu_pause.executar(self.game_state, self.events)

        elif self.game_state == SAIR:
            self.running = False
        pygame.display.flip()

    def update(self):
        if self.player.vidas <= 0:
            self.game_state = MORTO

        if self.game_state == MORTO:
            self.fase = self.fase_atual_tipo(self.screen, self.player)
            self.player.vidas = self.player.max_vidas
            self.player.is_invulnerable = False
            self.player.visible = True
            self.player.rect.center = self.screen.get_rect().center
            self.game_state = RODANDO
            return
        
        if self.game_state == RODANDO:
            self.player.trade_weapons()
            self.player.aim()
            self.player.shoot(self.delta_time)
            self.player.update(self.delta_time)
            
            # Atualiza todos os tiros do jogador de uma vez
            self.player.shots.update(self.delta_time)
            # Remove as balas que saem da tela
            for bala in self.player.shots:
                if not self.screen.get_rect().colliderect(bala.rect):
                    bala.kill()
            
            self.fase.update(self.delta_time)

    def go_to_next_level(self):
    
        print("Fase concluída!")
        self.current_level_index += 1

        # Verifica se ainda há fases na lista
        if self.current_level_index < len(self.levels):
            # Carrega a próxima fase
            self.fase_atual_tipo = self.levels[self.current_level_index]
            self.fase = self.fase_atual_tipo(self.screen, self.player)
        else:
            # Se não houver mais fases, o jogo acaba
            print("VOCÊ VENCEU O JOGO!")

            self.running = False

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
        pygame.quit()

if __name__ == '__main__':
    Game().run()