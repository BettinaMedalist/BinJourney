from utils.game_object import*

class Fase(GameObject):
    def __init__(self, screen, image_path, delta_time):
        super().__init__(screen, image_path)
        self.enemies = []
        self.objects = []
        self.delta_time = delta_time

    def add_enemy(self, enemy_type, x, y):
        pass

    def add_object(self, object_type, x, y):
        pass

    def movement(self, player):
        self.rect.x += (player.left - player.right) * self.delta_time * player.running
        self.rect.y += (player.up - player.down) * self.delta_time * player.running