from classes.game_object import*

class Inimigo(GameObject):
    def __init__(self, screen, image_path, x = 0, y = 0):
        super().__init__(screen, image_path, x, y)
        self.vidas = 10