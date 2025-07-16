from constantes import*
from jogador import*
from menu import MenuPrincipal, MenuPause 
from hud import*
from fases.tutorial import*
from fases.fase1 import*

class Game:
    def __init__(self):
        pygame.init()

        #Título do jogo
        pygame.display.set_caption("Bin Journey")

        #Janela do jogo
        self.screen = pygame.display.set_mode((16 * RES, 9 * RES))

        self.clock = pygame.time.Clock()
        self.delta_time = self.clock.tick(FPS)/1000

        #Estado do jogo
        self.game_state = MENU
        self.running = True

        self.hud = Hud(self.screen)

        self.player = Player(self.screen)
        self.player.rect.center = self.screen.get_rect().center
        self.player.shooting = False
        
        #Fase atual
        self.fase = Tutorial(self.screen, self.player)
        self.menu_principal = MenuPrincipal(self.screen)
        self.menu_pause = MenuPause(self.screen)

    #Função que checa inputsd
    def handle_events(self):
        self.delta_time = self.clock.tick(FPS)/1000

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                #Quando a tecla é apertada
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.game_state == RODANDO:
                            self.game_state = PAUSADO
                        elif self.game_state == PAUSADO:
                            self.game_state = RODANDO

                    if event.key == pygame.K_1:
                        self.player.arma = MAO
                    elif event.key == pygame.K_2:
                        self.player.arma = PISTOLA
                    elif event.key == pygame.K_3:
                        self.player.arma = METRALHADORA
                    elif event.key == pygame.K_4:
                        self.player.arma = MELEE
                    if event.key == pygame.K_RIGHT:
                        self.player.angle = DIREITA
                        self.player.shooting = True
                    elif event.key == pygame.K_UP:
                        self.player.angle = CIMA
                        self.player.shooting = True
                    elif event.key == pygame.K_LEFT:
                        self.player.angle = ESQUERDA
                        self.player.shooting = True
                    elif  event.key == pygame.K_DOWN:
                        self.player.angle = BAIXO
                        self.player.shooting = True
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
                    elif event.key == pygame.K_r:
                        if self.player.arma == PISTOLA:
                            self.player.m_pistola = 10
                        elif self.player.arma == METRALHADORA:
                            self.player.m_metralhadora = 30
                
                #Quando as teclas são soltas
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.player.shooting = False
                    if event.key == pygame.K_UP:
                        self.player.shooting = False
                    if event.key == pygame.K_LEFT:
                        self.player.shooting = False
                    if  event.key == pygame.K_DOWN:
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

    #Renderiza todos os objetos
    def render(self):
        self.screen.fill('yellow')
        if self.game_state == MENU:
            self.game_state = self.menu_principal.executar(self.game_state)
        elif self.game_state == RODANDO:
            self.fase.render()
            self.player.draw()
            for bala in self.player.shots:
                bala.draw()
            self.hud.mostrar_vida(self.player)
            self.hud.mostrar_arma(self.player)
        elif self.game_state == PAUSADO:
            self.fase.render()
            self.player.draw()
            for bala in self.player.shots:
                bala.draw()
            self.game_state = self.menu_pause.executar(self.game_state)
        elif self.game_state == SAIR:
            self.running = False
        pygame.display.flip()

    #Lida com o comportamento das entidades
    def update(self):
        if self.game_state == RODANDO:
            self.player.trade_weapons()
            self.player.aim()
            self.player.shoot(self.delta_time)

            self.player.update(self.delta_time)
            
            for bala in self.player.shots:
                bala.update(self.delta_time)
                if not self.screen.get_rect().colliderect(bala.rect):
                    self.player.shots.remove(bala)
            
            self.fase.update(self.delta_time)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()

        pygame.quit()

Game().run()