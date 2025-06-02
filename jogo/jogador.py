from utils.game_object import*
from utils.funcoes import*
from constantes import*

class Player(GameObject):
    def __init__(self, image_path):
        super().__init__(image_path)
        self.vidas = 3
        self.arma = MAO
        """
        self.sprites = {
            "mao": carregar_imagem("jogo\sprites\player_mao")
        }
        """

    def player_movement(self):
        pass

    def aim(self, angle):
        self.angle = (angle) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def trade_weapons(self, weapon):
        self.arma = weapon
        #Depois fazer umas comparações que dependendo da arma troca o sprite do player

    def collision(self):
        pass