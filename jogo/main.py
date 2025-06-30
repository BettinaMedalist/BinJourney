from constantes import*
from jogador import*
from menu import*
from hud import*
from fases.tutorial import*
from fases.fase1 import*

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Bin Journey")
        self.screen = pygame.display.set_mode((16 * RES, 9 * RES))

        self.clock = pygame.time.Clock()
        self.delta_time = self.clock.tick(FPS)/1000

        self.game_state = MENU
        self.running = True

        self.hud = Hud(self.screen)

        self.player = Player(self.screen)
        self.player.rect.center = self.screen.get_rect().center
        self.player.shooting = False

        self.fase = Tutorial(self.screen, self.player, self.delta_time)

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
                        if self.game_state != MENU:
                            self.game_state = PAUSADO

                    #Trocar de arma
                    if event.key == pygame.K_1:
                        self.player.arma = MAO
                    elif event.key == pygame.K_2:
                        self.player.arma = PISTOLA
                    elif event.key == pygame.K_3:
                        self.player.arma = METRALHADORA
                    elif event.key == pygame.K_4:
                        self.player.arma = MELEE

                    #Mirar e atirar
                    if event.key == pygame.K_RIGHT:
                        self.player.angle = DIREITA
                    elif event.key == pygame.K_UP:
                        self.player.angle = CIMA
                    elif event.key == pygame.K_LEFT:
                        self.player.angle = ESQUERDA
                    elif  event.key == pygame.K_DOWN:
                        self.player.angle = BAIXO

                    if event.key == pygame.K_w:
                        self.player.up = self.player.speed
                    if event.key == pygame.K_a:
                        self.player.left = self.player.speed
                    if event.key == pygame.K_s:
                        self.player.down = self.player.speed
                    if event.key == pygame.K_d:
                        self.player.right = self.player.speed
                    
                    if event.key == pygame.K_LSHIFT:
                        self.player.running = 3

                    elif event.key == pygame.K_SPACE:
                        self.player.shooting = True

                    elif event.key == pygame.K_r:
                        if self.player.arma == PISTOLA:
                            self.player.m_pistola = 10
                        elif self.player.arma == METRALHADORA:
                            self.player.m_metralhadora = 30

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.player.shooting = False
                    
                    if event.key == pygame.K_w:
                        self.player.up = 0
                    if event.key == pygame.K_s:
                        self.player.down = 0
                    if event.key == pygame.K_a:
                        self.player.left = 0 
                    if event.key == pygame.K_d:
                        self.player.right = 0

                    if event.key == pygame.K_LSHIFT:
                        self.player.running = 1

    def render(self):
        self.screen.fill('yellow')
        if self.game_state == MENU:
            self.game_state = mostrar_menu(self.screen, self.game_state)

        elif self.game_state == RODANDO:
            self.fase.render()
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

        self.player.shoot(self.delta_time)
        
        for bala in self.player.shots:
            bala.update(self.delta_time)
            if not self.screen.get_rect().colliderect(bala.rect):
                self.player.shots.remove(bala)
        
        self.fase.movement(self.player)
        self.fase.running()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()

    pygame.quit()

Game().run()  