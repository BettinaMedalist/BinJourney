from constantes import*
from utils.botao import*

class MenuPrincipal:
    def __init__(self, screen):
        self.screen = screen
        
        # Caminhos corrigidos e botões criados uma única vez
        b_jogar = Botao(screen, "jogo/sprites/jogar.png")
        b_sair = Botao(screen, "jogo/sprites/sair.png")

        b_jogar.rect.centerx = screen.get_rect().centerx
        b_jogar.rect.centery = screen.get_rect().centery - 100

        b_sair.rect.centerx = screen.get_rect().centerx
        b_sair.rect.centery = screen.get_rect().centery + 100
        
        self.botoes = {
            "jogar": b_jogar,
            "sair": b_sair
        }

    def executar(self, game_state, events):
        self.botoes["jogar"].draw()
        self.botoes["sair"].draw()

        for event in events:
            if self.botoes["jogar"].handle_event(event):
                    return RODANDO
            elif self.botoes["sair"].handle_event(event):
                return SAIR
        
        return game_state

class MenuPause:
    def __init__(self, screen):
        self.screen = screen
        
        # Botão de configurações removido
        b_voltar = Botao(screen, "jogo/sprites/jogar.png")
        b_menu_principal = Botao(screen, "jogo/sprites/sair.png")

        # Posições ajustadas para os botões restantes
        b_voltar.rect.centerx = screen.get_rect().centerx
        b_voltar.rect.centery = screen.get_rect().centery - 100 # Um pouco acima do centro

        b_menu_principal.rect.centerx = b_voltar.rect.centerx
        b_menu_principal.rect.top = b_voltar.rect.bottom + 100
        
        self.botoes = {
            "voltar": b_voltar,
            "menu_principal": b_menu_principal
            # Entrada "config" removida
        }

    def executar(self, game_state, events):
        self.botoes["voltar"].draw()
        # Linha para desenhar o botão de config removida
        self.botoes["menu_principal"].draw()

        for event in events:
            if self.botoes["voltar"].handle_event(event):
                return RODANDO
            # Condição para o botão de config removida
            elif self.botoes["menu_principal"].handle_event(event):
                return MENU
            
        return game_state