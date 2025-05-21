import pygame
from config import*
from game_state import*
#from jogador import*
from menu import*

pygame.init()

LARGURA_TELA = RES * 16
ALTURA_TELA = RES * 9
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
clock = pygame.time.Clock()

game_state = 0
rodando = True

while rodando:
    mouse_button = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_button = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = PAUSADO
        
    tela.fill('YELLOW')

    if game_state == MENU:
        game_state = mostrar_menu(tela, game_state)

    #elif game_state == RODANDO:
        
    #elif game_state == CONFIG:

    elif game_state == PAUSADO:
        game_state = mostrar_pause(tela, game_state)

    elif game_state == SAIR:
        rodando = False

    pygame.display.flip()

    print(game_state)

    delta_time = clock.tick(FPS)/1000

pygame.quit()   