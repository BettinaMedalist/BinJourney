#tela inicial, pausa
import pygame
import sys
import time
from utils.funcoes import*
from game_state import*
from utils.game_object import GameObject

pygame.init()


def mostrar_menu(tela, game_state):
    b_jogar = GameObject("assets\imagens\jogar.png")
    b_config = GameObject("assets\imagens\configuracoes.png")
    b_sair = GameObject(("assets\imagens\sair.png"))

    b_jogar.set_position(meio(b_jogar, tela), 200)
    b_config.set_position(meio(b_config, tela), b_jogar.y + b_jogar.height + 20)
    b_sair.set_position(meio(b_sair, tela), b_config.y + b_config.height + 20)

    b_jogar.draw(tela)
    b_config.draw(tela)
    b_sair.draw(tela)

    if apertado(b_jogar):
        game_state = RODANDO
    elif apertado(b_config):
        game_state = CONFIG
    elif apertado(b_sair):
        game_state = SAIR
    return game_state

def mostrar_pause(tela, game_state):
    b_voltar = GameObject("assets\imagens\sair.png")
    b_config = GameObject("assets\imagens\configuracoes.png")
    b_menu_principal = GameObject("assets\imagens\life.png")

    b_voltar.set_position(meio(b_voltar, tela), 200)
    b_config.set_position(meio(b_config, tela), b_voltar.y + b_voltar.height + 20)
    b_menu_principal.set_position(meio(b_menu_principal, tela), b_config.y + b_config.height + 20)

    b_voltar.draw(tela)
    b_config.draw(tela)
    b_menu_principal.draw(tela)


    if apertado(b_voltar):
        game_state = RODANDO
    elif apertado(b_config):
        game_state = CONFIG
    elif apertado(b_menu_principal):
        game_state = MENU
        time.sleep(0.1)
    return game_state