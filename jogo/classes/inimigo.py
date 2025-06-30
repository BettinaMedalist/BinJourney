from classes.game_object import*

class Inimigo(GameObject):
    def __init__(self, screen, image_path, angle, x = 0, y = 0):
        super().__init__(screen, image_path, x, y)
        self.vidas = 3
        original_image = self.image
        rotated_image = pygame.transform.rotate(original_image, angle)
        self.image = rotated_image

class Inimigo_Pistola(Inimigo):
    def __init__(self, screen, angle, x, y):
        super().__init__(screen, "jogo\sprites\inimigo_pistola.png", angle, x, y)