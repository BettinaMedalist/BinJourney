from constantes import*
from classes.game_object import*

class Hud():
    def __init__(self, screen):
        self.screen = screen

        self.arma_sprite = {
            "pistola": GameObject(self.screen, "jogo/sprites/pistola_hud.png", self.screen.get_width() - 150, self.screen.get_height() - 150),
            "metralhadora": GameObject(self.screen, "jogo/sprites/rifle_hud.png", self.screen.get_width() - 150, self.screen.get_height() - 150)
        }
        self.arma = self.arma_sprite["metralhadora"]

        self.max_vidas = 3
        self.vidas_sprites = []
        for i in range(self.max_vidas):
            self.vidas_sprites.append(GameObject(self.screen, "jogo/sprites/life.png", 20 + i * 50, 20))

    def mostrar_vida(self, player):
        for i in range(player.vidas):
            self.vidas_sprites[i].draw()

    def mostrar_arma(self, player):
        if player.arma == PISTOLA:
            self.arma = self.arma_sprite["pistola"]
            self.arma.draw()
        elif player.arma == METRALHADORA:
            self.arma = self.arma_sprite["metralhadora"]
            self.arma.draw()