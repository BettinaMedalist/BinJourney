from classes.fase import*
class Fase1(Fase):
    def __init__(self, screen, player, delta_time):
        super().__init__(screen, "jogo\sprites\paredes.png", player, delta_time)