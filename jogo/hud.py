from constantes import*
from utils.funcoes import carregar_imagem
from utils.game_object import*

#Para desenhar na tela o hud
class Hud():
    def __init__(self, tela):
        self.tela = tela

    def mostrar_vida(self, player):
        vidas = []
        for i in range(player.vidas):
            vidas.append(GameObject("jogo\sprites\life.png", i * 70))
    
        for vida in vidas:
            vida.draw(self.tela)

    def mostrar_arma(self, player):
        pass
        slot_arma = player.arma
        #if slot_arma == MAO:
            