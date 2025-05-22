from utils.game_object import GameObject

class Player(GameObject):
    def __init__(self, image_path):
        super().__init__(image_path)
        self.vidas = 3

    def player_movement(self):
        pass

    def collision(self):
        pass