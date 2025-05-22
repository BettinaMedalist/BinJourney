from utils.funcoes import carregar_imagem
from utils.game_object import*

#Para desenhar na tela o hud
def mostrar_hud(tela, player):
    #slot_arma = carregar_imagem()
    vidas = []
    for i in range(player.vidas):
        vidas.append(GameObject("jogo\sprites\life.png", i * 70))
    
    for vida in vidas:
        vida.draw(tela)