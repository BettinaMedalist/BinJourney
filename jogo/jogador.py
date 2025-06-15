from classes.tiro import*
from constantes import*

class Player(GameObject):
    def __init__(self, screen, image_path):
        super().__init__(screen, image_path)
        self.vidas = 3
        self.arma = MAO
        self.sprites = {
            "mao": carregar_imagem("jogo\sprites\player_semarma.png"),
            "pistola": carregar_imagem("jogo\sprites\player_pistola.png"),
            "metralhadora": carregar_imagem("jogo\sprites\player_metralhadora.png")
        }

        self.shots = []
        
        self.original_image = self.image

    def aim(self):
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        self.image = rotated_image
        self.rect = new_rect
    
    def shoot(self):
        self.shots.append(Tiro(self.screen, "jogo\sprites\player.png", self))

    def trade_weapons(self):
        if self.arma == MAO:
            self.original_image = self.sprites["mao"]
        elif self.arma == PISTOLA:
            self.original_image = self.sprites["pistola"]
        elif self.arma == METRALHADORA:
            self.original_image = self.sprites["metralhadora"]
        
        self.rect = self.original_image.get_rect(center=self.rect.center)
        self.image = self.original_image

    def collision(self):
        pass