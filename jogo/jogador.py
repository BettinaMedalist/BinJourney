from classes.tiro import*
from constantes import*

class Player(GameObject):
    def __init__(self, screen):
        super().__init__(screen, "jogo\sprites\player_semarma.png")
        self.vidas = 3

        self.speed = 700
        
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0
        self.running = 1

        self.direction = pygame.math.Vector2()

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

        self.shots = pygame.sprite.Group() #self.shots = [], agr é no groups
        
        self.original_image = self.image
    
    def update(self, walls_group, delta_time, all_sprites_group):
        # 1. Converte os inputs (up, down, left, right) em um vetor de direção
        # (Aqui está o "elo perdido" que corrigimos)
        mov_x = self.right - self.left
        mov_y = self.down - self.up
        self.direction = pygame.math.Vector2(mov_x, mov_y)

        # 2. Chama os outros métodos do jogador
        self.aim()
        self.shoot(delta_time, all_sprites_group)
        # O trade_weapons é melhor ser chamado só no evento de troca de tecla


    def aim(self):
        centro_antigo = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=centro_antigo)
    
    def shoot(self, delta_time, all_sprites_group):
        self.cadence_metralhadora += delta_time
        if self.shooting:
            tiro_criado = None

            if self.arma == PISTOLA and self.m_pistola > 0:
                tiro_criado = Tiro(self.screen, self)
                self.m_pistola -= 1
                self.shooting = False #single shot
            
            elif self.arma == METRALHADORA and self.m_metralhadora > 0 and self.cadence_metralhadora >= 0.1:
                tiro_criado = Tiro(self.screen, self)
                self.m_metralhadora -= 1
                self.cadence_metralhadora = 0
                
            if tiro_criado:
                self.shots.add(tiro_criado)
                all_sprites_group.add(tiro_criado)


    def trade_weapons(self, nova_arma):
        if self.arma == nova_arma:
            return
        self.arma = nova_arma # Atualiza a arma
        centro_antigo = self.rect.center

        if self.arma == MAO:
            self.original_image = self.sprites["mao"]
            #tem q definir como a melee funfa
        elif self.arma == PISTOLA:
            self.original_image = self.sprites["pistola"]
            self.arma_cadencia = 0.5
            self.arma_dano = 2

        elif self.arma == METRALHADORA:
            self.original_image = self.sprites["metralhadora"]
            self.arma_cadencia = 0.15
            self.arma_dano = 1
        
        self.rect = self.original_image.get_rect(center=centro_antigo)

    def movement(self):
        pass