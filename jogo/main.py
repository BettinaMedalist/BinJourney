import pygame
from constantes import*
from jogador import*
from menu import*
from hud import*

class Game:
    def __init__(self):
        pygame.init()

        LARGURA_TELA = 800
        ALTURA_TELA = 600
        pygame.display.set_caption("Bin Journey")
        self.screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

        self.clock = pygame.time.Clock()

        self.game_state = MENU
        self.running = True

        self.hud = Hud(self.screen)
        self.player = Player("jogo\sprites\player.png", self.screen)
        self.player.set_position(meio("x", self.player, self.screen), meio("y", self.player, self.screen))

    def handle_events(self):
        for event in pygame.event.get():
                #Fechar o jogo
                if event.type == pygame.QUIT:
                    self.running = False

                #Teclas do teclado
                elif event.type == pygame.KEYDOWN:
                    #Pausar o jogo
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = PAUSADO
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


                    

    def render(self):
        self.screen.fill('YELLOW')
        if self.game_state == MENU:
            self.game_state = mostrar_menu(self.screen, self.game_state)

        elif self.game_state == RODANDO:
            self.player.draw(self.screen)
            self.hud.mostrar_vida(self.player)
        
        #elif game_state == CONFIG:

        elif self.game_state == PAUSADO:
            self.game_state = mostrar_pause(self.screen, self.game_state)

        elif self.game_state == SAIR:
            self.game_state = False

        pygame.display.flip()

    def update(self):
        self.player.trade_weapons()
        self.player.aim()

    def run(self):
        while self.running:
            self.handle_events()
            self.render()
            self.update()

        delta_time = self.clock.tick(FPS)/1000

    pygame.quit()

Game().run()  