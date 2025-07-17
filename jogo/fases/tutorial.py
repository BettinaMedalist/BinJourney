from classes.fase import *
from constantes import *
from classes.tile import*

# A matriz continua a mesma por enquanto, você a modificará depois com os novos códigos
TUTORIAL_LAYOUT = [
    'WWWWWWWWWWWWWWWWWWWWWWWW',
    'W                      W',
    'W          P           W',
    'W                      W',
    'W                      W',
    'W                      W',
    'W                      W',
    'W                      W',
    'W                      W',
    'W                      W',
    'W                      W',
    'W                      W',
    'W                      W',
    'W                      W',
    'W                      W',
    'W                      W',
    'W         F            W',
    'W        ASD           W',
    'W         J            W',
    'W                      W',
    'WWWWWWWWWWWWWWWWWWWWWWWW',
]
TILE_SIZE = 64


class Tutorial(Fase):
    def __init__(self, screen, player, delta_time):
        super().__init__(screen, player, delta_time)

        # Carrega as imagens dos tiles
        self.chao_tile_img = pygame.image.load("jogo/sprites/chaoconcreto.png").convert_alpha()
        self.parede_tile_img = pygame.image.load("jogo/sprites/paredetuto.png").convert_alpha()
        self.W_tile_img = pygame.image.load("jogo/sprites/W.png").convert_alpha()
        self.A_tile_img = pygame.image.load("jogo/sprites/A.png").convert_alpha()
        self.S_tile_img = pygame.image.load("jogo/sprites/S.png").convert_alpha()
        self.D_tile_img = pygame.image.load("jogo/sprites/D.png").convert_alpha()

        # Loop que lê a matriz e constrói o nível
        for row_index, row in enumerate(TUTORIAL_LAYOUT):
            for col_index, tile_code in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                # Lógica para o chão (desenhado sob todos os objetos)
                if tile_code != 'W':
                    Tile(self.chao_tile_img, x, y, groups=[self.background_group])

                # Lógica para os objetos específicos
                if tile_code == 'W':
                    Tile(self.parede_tile_img, x, y, groups=[self.background_group])
                    self.add_object("parede", 0, x, y)


                elif tile_code == 'J':  # J = Jogador
                    self.player.rect.topleft = (x, y)

                elif tile_code == 'G':  # G = Inimigo com Pistola
                    self.add_enemy("pistola", 0, x, y)

                elif tile_code == 'M':  # M = Inimigo com Metralhadora
                    self.add_enemy("metralhadora", 0, x, y)

                elif tile_code == 'K':  # K = Inimigo Melee
                    self.add_enemy("melee", 0, x, y)

                elif tile_code == 'P':  # P = Inimigo de Patrulha com Pistola
                    # Como mencionado, o ponto B da patrulha não pode vir do mapa.
                    # Teríamos que definir um ponto padrão aqui, ou criá-lo de forma diferente.
                    # Por enquanto, criamos ele sem um ponto B (ponto_b=None).
                    self.add_enemy("pistola_patrulha", 0, x, y, ponto_b=None)
                elif tile_code == "F":
                    Tile(self.W_tile_img,x,y, groups=[self.background_group])
                elif tile_code == "A":
                    Tile(self.A_tile_img,x,y, groups=[self.background_group])
                elif tile_code == "S":
                    Tile(self.S_tile_img,x,y, groups=[self.background_group])
                elif tile_code == "D":
                    Tile(self.D_tile_img,x,y, groups=[self.background_group])
        screen_center_x = self.screen.get_rect().centerx
        screen_center_y = self.screen.get_rect().centery

        shift_x = self.player.rect.centerx - screen_center_x
        shift_y = self.player.rect.centery - screen_center_y

        for group in self.world_groups:
            for sprite in group:
                sprite.rect.x -= shift_x
                sprite.rect.y -= shift_y
        
        for shot in self.player.shots:
            shot.rect.x -= shift_x
            shot.rect.y -= shift_y

        self.player.rect.x -= shift_x
        self.player.rect.y -= shift_y