from constantes import*
from utils.botao import*

class MenuPrincipal:
    def __init__(self, screen):
        self.screen = screen
        
        # Caminhos corrigidos e botões criados uma única vez
        b_jogar = Botao(screen, "jogo/sprites/jogar.png")
        b_config = Botao(screen, "jogo/sprites/configuracoes.png")
        b_sair = Botao(screen, "jogo/sprites/sair.png")

        b_config.rect.center = screen.get_rect().center
        b_jogar.rect.centerx = b_config.rect.centerx
        b_jogar.rect.bottom = b_config.rect.top - 20
        b_sair.rect.centerx = b_config.rect.centerx
        b_sair.rect.top = b_config.rect.bottom + 20
        
        self.botoes = {
            "jogar": b_jogar,
            "config": b_config,
            "sair": b_sair
        }

    def executar(self, game_state):
        self.botoes["jogar"].draw()
        self.botoes["config"].draw()
        self.botoes["sair"].draw()

        if self.botoes["jogar"].apertado():
            return RODANDO
        elif self.botoes["config"].apertado():
            return CONFIG
        elif self.botoes["sair"].apertado():
            return SAIR
        
        return game_state

class MenuPause:
    def __init__(self, screen):
        self.screen = screen
        
        b_voltar = Botao(screen, "jogo/sprites/jogar.png")
        b_config = Botao(screen, "jogo/sprites/configuracoes.png")
        b_menu_principal = Botao(screen, "jogo/sprites/sair.png")

        b_config.rect.center = screen.get_rect().center
        b_voltar.rect.centerx = b_config.rect.centerx
        b_voltar.rect.bottom = b_config.rect.top - 20
        b_menu_principal.rect.centerx = b_config.rect.centerx
        b_menu_principal.rect.top = b_config.rect.bottom + 20
        
        self.botoes = {
            "voltar": b_voltar,
            "config": b_config,
            "menu_principal": b_menu_principal
        }

    def executar(self, game_state):
        self.botoes["voltar"].draw()
        self.botoes["config"].draw()
        self.botoes["menu_principal"].draw()

        if self.botoes["voltar"].apertado():
            return RODANDO
        elif self.botoes["config"].apertado():
            return CONFIG
        elif self.botoes["menu_principal"].apertado():
            return MENU
            
        return game_state