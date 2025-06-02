import pygame
from config import*
from game_state import*
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

        self.player = Player("jogo\sprites\player.png")
        self.player.set_position(meio("x", self.player, self.screen), meio("y", self.player, self.screen))

    def handle_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = PAUSADO

    def render(self):
        self.screen.fill('YELLOW')
        if self.game_state == MENU:
            self.game_state = mostrar_menu(self.screen, self.game_state)

        elif self.game_state == RODANDO:
            self.player.draw(self.screen)
            mostrar_hud(self.screen, self.player)
        
        #elif game_state == CONFIG:

        elif self.game_state == PAUSADO:
            self.game_state = mostrar_pause(self.screen, self.game_state)

        elif self.game_state == SAIR:
            self.game_state = False

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.render()
            

        delta_time = self.clock.tick(FPS)/1000

    pygame.quit()

Game().run()  