from constantes import*
from jogador import*
from menu import*
from hud import*
from fases.tutorial import*

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Bin Journey")
        self.screen = pygame.display.set_mode((16 * RES, 9 * RES))

        self.clock = pygame.time.Clock()
        self.delta_time = self.clock.tick(FPS)/1000

        self.mouse = False

        self.game_state = MENU
        self.running = True

        self.hud = Hud(self.screen)
        self.player = Player(self.screen, "jogo\sprites\player.png")
        self.player.rect.center = self.screen.get_rect().center
        self.player_shooting = False

    def handle_events(self):
        self.delta_time = self.clock.tick(FPS)/1000

        for event in pygame.event.get():
                #Fechar o jogo
                if event.type == pygame.QUIT:
                    self.running = False

                #Teclas do teclado
                elif event.type == pygame.KEYDOWN:
                    #Pausar o jogo
                    if event.key == pygame.K_ESCAPE:
                        if self.game_state == RODANDO:
                            self.game_state = PAUSADO

                    elif event.key == pygame.MOUSEBUTTONDOWN:
                        self.mouse = True

                    #Trocar de arma
                    elif event.key == pygame.K_1:
                        self.player.arma = MAO
                    elif event.key == pygame.K_2:
                        self.player.arma = PISTOLA
                    elif event.key == pygame.K_3:
                        self.player.arma = METRALHADORA
                    elif event.key == pygame.K_4:
                        self.player.arma = MELEE

                    #Mirar e atirar
                    elif event.key == pygame.K_RIGHT:
                        self.player.angle = DIREITA
                    elif event.key == pygame.K_UP:
                        self.player.angle = CIMA
                    elif event.key == pygame.K_LEFT:
                        self.player.angle = ESQUERDA
                    elif  event.key == pygame.K_DOWN:
                        self.player.angle = BAIXO
                    
                    elif event.key == pygame.K_SPACE:
                        self.player_shooting = True

                    else:
                        self.mouse = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.player_shooting = False

    def render(self):
        self.screen.fill('YELLOW')
        if self.game_state == MENU:
            self.game_state = mostrar_menu(self.screen, self.game_state)

        elif self.game_state == RODANDO:
            Tutorial(self.screen, "jogo\sprites\FUNDOTESTE1-sheet.png").draw()
            self.player.draw()
            self.hud.mostrar_vida(self.player)
            self.hud.mostrar_arma(self.player)
            for bala in self.player.shots:
                bala.draw()
        
        #elif game_state == CONFIG:

        elif self.game_state == PAUSADO:
            self.game_state = mostrar_pause(self.screen, self.game_state)

        elif self.game_state == SAIR:
            self.game_state = False

        pygame.display.flip()

    def update(self):
        self.player.trade_weapons()
        self.player.aim()

        if self.player_shooting and not self.player.arma == MAO:
            self.player.shoot()
        
        for bala in self.player.shots:
            bala.update(self.delta_time)
            if not self.screen.get_rect().colliderect(bala.rect):
                self.player.shots.remove(bala)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()

    pygame.quit()

Game().run()  