from utils.game_object import*

class Fase(GameObject):
    def __init__(self, screen, image_path):
        super().__init__(screen, image_path)
        self.enemies = []
        self.objects = []

    def add_enemy(self, enemy_type, x, y):
        pass

    def add_object(self, object_type, x, y):
        pass

    def movement(self):
        pass