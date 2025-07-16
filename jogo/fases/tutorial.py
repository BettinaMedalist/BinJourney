from classes.fase import *
from constantes import *
# A classe Tile provavelmente está em outro lugar, ajuste o import se necessário
from classes.tile import Tile

# A matriz continua a mesma por enquanto, você a modificará depois com os novos códigos
TUTORIAL_LAYOUT = [
    'WWWWWWWWWWWWWWWWWWWWWWW',
    'W                 W    W',
    'W                 W    W',
    'W                 W    W',
    'W             E   W    W',
    'W         P       W    W',
    'W                 W    W',
    'W                 W    W',
    'W                 W    W',
    'W                 W    W',
    'W                 W    W',
    'WWWWWWWWWWWWWWWWWWWWWWW',
]
TILE_SIZE = 64

class Tutorial(Fase):
    def __init__(self, screen, player, delta_time):
        super().__init__(screen, player, delta_time)

        # Carrega as imagens dos tiles
        self.chao_tile_img = pygame.image.load("jogo/sprites/chaotuto.png").convert_alpha()
        self.parede_tile_img = pygame.image.load("jogo/sprites/paredetuto.png").convert_alpha()

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

                # --- LÓGICA ATUALIZADA COM OS NOVOS CÓDIGOS ---

                elif tile_code == 'J': # J = Jogador
                    self.player.rect.topleft = (x, y)

                elif tile_code == 'G': # G = Inimigo com Pistola
                    self.add_enemy("pistola", 0, x, y)

                elif tile_code == 'M': # M = Inimigo com Metralhadora
                    self.add_enemy("metralhadora", 0, x, y)

                elif tile_code == 'K': # K = Inimigo Melee
                    self.add_enemy("melee", 0, x, y)

                elif tile_code == 'P': # P = Inimigo de Patrulha com Pistola
                    # Como mencionado, o ponto B da patrulha não pode vir do mapa.
                    # Teríamos que definir um ponto padrão aqui, ou criá-lo de forma diferente.
                    # Por enquanto, criamos ele sem um ponto B (ponto_b=None).
                    self.add_enemy("pistola_patrulha", 0, x, y, ponto_b=None)