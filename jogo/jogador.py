from classes.tiro import*
from constantes import*

class Player(GameObject):
    def __init__(self, screen):
        super().__init__(screen, "jogo\sprites\player_semarma.png")
        self.vidas = 3

        self.speed = 100
        
        self.left = 0
        self.right = 0
        self.up = 0
        self.down = 0

        self.running = 1

        self.m_pistola = 10
        self.m_metralhadora = 30
        self.cadence_metralhadora = 0

        self.shooting = False

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
    
    def shoot(self, delta_time):
        self.cadence_metralhadora += delta_time
        if self.shooting:
            if self.arma == PISTOLA and self.m_pistola > 0:
                self.shots.append(Tiro(self.screen, self))
                self.m_pistola -= 1
                self.shooting = False
            
            elif self.arma == METRALHADORA and self.m_metralhadora > 0 and self.cadence_metralhadora >= 0.1:
                self.shots.append(Tiro(self.screen, self))
                self.m_metralhadora -= 1
                self.cadence_metralhadora = 0
            if self.m_metralhadora <= 0:
                self.shooting = False
            cadence = True


    def trade_weapons(self):
        if self.arma == MAO:
            self.original_image = self.sprites["mao"]
        elif self.arma == PISTOLA:
            self.original_image = self.sprites["pistola"]
        elif self.arma == METRALHADORA:
            self.original_image = self.sprites["metralhadora"]
        
        self.rect = self.original_image.get_rect(center=self.rect.center)
        self.image = self.original_image

    def movement(self):
        pass