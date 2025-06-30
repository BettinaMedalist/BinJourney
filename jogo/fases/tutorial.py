from classes.fase import*
from constantes import*

class Tutorial(Fase):
    def __init__(self, screen, player, delta_time):
        super().__init__(screen, "jogo\sprites\FUNDOTESTE1-sheet.png", player, delta_time)
        self.add_enemy(0, ESQUERDA, 1, 1)
        self.add_enemy(0, CIMA, 300, 500)
        self.add_enemy(0, DIREITA, 150, 180)
        self.add_enemy(0, BAIXO, 700, 100)
        self.add_enemy(0, ESQUERDA, 650, 800)
        self.add_enemy(0, 170, 70, 400)
    