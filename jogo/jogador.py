from utils.game_object import*
from utils.funcoes import*
from constantes import*

class Player(GameObject):
    def __init__(self, image_path, tela):
        super().__init__(image_path)
        self.vidas = 3
        self.arma = MAO
        self.screen = tela
        self.sprites = {
            "mao": carregar_imagem("jogo\sprites\player_semarma.png"),
            "pistola": carregar_imagem("jogo\sprites\player_pistola.png"),
            "metralhadora": carregar_imagem("jogo\sprites\player_metralhadora.png")
        }


    def player_movement(self):
        pass

    def aim(self):
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def trade_weapons(self):
        if self.arma == MAO:
            self.image = self.sprites["mao"]
        elif self.arma == PISTOLA:
            self.image = self.sprites["pistola"]
        elif self.arma == METRALHADORA:
            self.image = self.sprites["metralhadora"]
        self.set_position(meio("x", self, self.screen), meio("y", self, self.screen))



    def collision(self):
        pass