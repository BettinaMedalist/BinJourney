#tela inicial, pausa
from constantes import*
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


def mostrar_menu(screen, game_state):
    b_jogar = Botao(screen, "jogo\sprites\jogar.png")
    b_config = Botao(screen, "jogo\sprites\configuracoes.png")
    b_sair = Botao(screen, "jogo\sprites\sair.png")

    b_config.rect.center = screen.get_rect().center

    b_jogar.rect.centerx = b_config.rect.centerx
    b_jogar.rect.bottom = b_config.rect.top - 20

    b_sair.rect.centerx = b_config.rect.centerx
    b_sair.rect.top = b_config.rect.bottom + 20

    b_jogar.draw()
    b_config.draw()
    b_sair.draw()

    if b_jogar.apertado():
        game_state = RODANDO
    elif b_config.apertado():
        game_state = CONFIG
    elif b_sair.apertado():
        pass
        # game_state = SAIR
    return game_state

def mostrar_pause(screen, game_state):
    #Problema na hora de clicar no botão de voltar para o menu devido ao problema em utils\funcoes\apertado
    b_voltar = Botao(screen, "jogo\sprites\sair.png")
    b_config = Botao(screen, "jogo\sprites\configuracoes.png")
    b_menu_principal = Botao(screen, "jogo\sprites\life.png")

    b_config.rect.center = screen.get_rect().center

    b_voltar.rect.centerx = b_config.rect.centerx
    b_voltar.rect.bottom = b_config.rect.top - 20

    b_menu_principal.rect.centerx = b_config.rect.centerx
    b_menu_principal.rect.top = b_config.rect.bottom + 20

    b_voltar.draw()
    b_config.draw()
    b_menu_principal.draw()


    if b_voltar.apertado():
        game_state = RODANDO
    elif b_config.apertado():
        game_state = CONFIG
    elif b_menu_principal.apertado():
        game_state = MENU
    return game_state