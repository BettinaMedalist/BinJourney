from classes.game_object import*

class Upgrade(GameObject):
    def __init__(self, screen, x, y):
        super().__init__(screen, "jogo/sprites/upgrade.png", x, y)
        self.hitbox = self.rect.inflate(-10, -10)