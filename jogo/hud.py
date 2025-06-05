from constantes import*
from utils.funcoes import carregar_imagem
from utils.game_object import*

#Para desenhar na tela o hud
class Hud():
    def __init__(self, tela):
        self.tela = tela
        #por enquanto so esses sprites
        self.arma_sprite = {
            "pistola": GameObject("jogo\sprites\\pistola_hud.png", tela.get_width() - 150, tela.get_height() - 150),
            "metralhadora": GameObject("jogo\sprites\\rifle_hud.png", tela.get_width() - 150, tela.get_height() - 150)
        }
        self.arma = self.arma_sprite["metralhadora"]

    def mostrar_vida(self, player):
        vidas = []
        for i in range(player.vidas):
            vidas.append(GameObject("jogo\sprites\life.png", 20 + i * 90, 20))
    
        for vida in vidas:
            vida.draw(self.tela)

    def mostrar_arma(self, player):
        if player.arma == PISTOLA:
            self.arma = self.arma_sprite["pistola"]
        elif player.arma == METRALHADORA:
            self.arma = self.arma_sprite["metralhadora"]
        self.arma.draw(self.tela)