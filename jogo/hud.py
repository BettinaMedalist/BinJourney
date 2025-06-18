from constantes import*
from classes.game_object import*

#Para desenhar na tela o hud
class Hud():
    def __init__(self, screen):
        #por enquanto so esses sprites
        self.screen = screen
        self.arma_sprite = {
            "pistola": GameObject(self.screen, "jogo\sprites\\pistola_hud.png", self.screen.get_width() - 150, self.screen.get_height() - 150),
            "metralhadora": GameObject(self.screen, "jogo\sprites\\rifle_hud.png", self.screen.get_width() - 150, self.screen.get_height() - 150)
        }
        self.arma = self.arma_sprite["metralhadora"]

    def mostrar_vida(self, player):
        vidas = []
        for i in range(player.vidas):
            vidas.append(GameObject(self.screen, "jogo\sprites\life.png", 20 + i * 90, 20))
    
        for vida in vidas:
            vida.draw()

    def mostrar_arma(self, player):
        if player.arma == PISTOLA:
            self.arma = self.arma_sprite["pistola"]
        elif player.arma == METRALHADORA:
            self.arma = self.arma_sprite["metralhadora"]
        self.arma.draw()