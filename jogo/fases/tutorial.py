from classes.fase import*
from constantes import*

class Tutorial(Fase):
    def __init__(self, screen, player):
        super().__init__(screen, "jogo/sprites/FUNDOTESTE1-sheet.png", player)
        self.add_enemy("pistola", ESQUERDA, 1, 1)
        self.add_enemy("pistola_patrulha", CIMA, 300, 1600, (700, 900))
        self.add_enemy("metralhadora", DIREITA, 150, 180)
        self.add_enemy("pistola", BAIXO, 700, 100)
        self.add_enemy("metralhadora", ESQUERDA, 650, 800)
        self.add_enemy("pistola", ESQUERDA, 70, 400)
        self.add_enemy("meelee", ESQUERDA, 800, 400)