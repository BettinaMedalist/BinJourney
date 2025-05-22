#tela inicial, pausa
import pygame
import sys
#from utils.funcoes import*
from game_state import*
from utils.game_object import*
from utils.botao import*

#Esse arquivo vai gerenciar os diferentes menus

"""
class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []

    def add_button(self, image, y, acao):
        botao = Botao(image)
        botao.set_position(meio("x", botao, self.screen), y)
        self.buttons.append((botao, acao))
"""     


def mostrar_menu(tela, game_state):
    b_jogar = Botao("jogo\sprites\jogar.png")
    b_config = Botao("jogo\sprites\configuracoes.png")
    b_sair = Botao(("jogo\sprites\sair.png"))

    b_jogar.set_position(meio("x", b_jogar, tela), 100)
    b_config.set_position(meio("x", b_config, tela), b_jogar.y + b_jogar.height + 20)
    b_sair.set_position(meio("x", b_sair, tela), b_config.y + b_config.height + 20)

    b_jogar.draw(tela)
    b_config.draw(tela)
    b_sair.draw(tela)

    if b_jogar.apertado():
        game_state = RODANDO
    elif b_config.apertado():
        game_state = CONFIG
    elif b_sair.apertado():
        pass
        # game_state = SAIR
    return game_state

def mostrar_pause(tela, game_state):
    #Problema na hora de clicar no botão de voltar para o menu devido ao problema em utils\funcoes\apertado
    b_voltar = Botao("jogo\sprites\sair.png")
    b_config = Botao("jogo\sprites\configuracoes.png")
    b_menu_principal = Botao("jogo\sprites\life.png")

    b_voltar.set_position(meio("x", b_voltar, tela), 100)
    b_config.set_position(meio("x", b_config, tela), b_voltar.y + b_voltar.height + 20)
    b_menu_principal.set_position(meio("x", b_menu_principal, tela), b_config.y + b_config.height + 20)

    b_voltar.draw(tela)
    b_config.draw(tela)
    b_menu_principal.draw(tela)


    if b_voltar.apertado():
        game_state = RODANDO
    elif b_config.apertado():
        game_state = CONFIG
    elif b_menu_principal.apertado():
        game_state = MENU
    return game_state