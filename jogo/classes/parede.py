from classes.game_object import*

class Parede(GameObject):
    def __init__(self, screen, x, y):
        super().__init__(screen, "jogo\sprites\parede.png", x, y)