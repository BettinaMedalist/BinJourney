from classes.fase import *
from constantes import *

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
        super().__init__(screen,player, delta_time)

        self.chao_tile_img = pygame.image.load("jogo/sprites/chaotuto.png").convert_alpha()
        self.parede_tile_img = pygame.image.load("jogo/sprites/paredetuto.png").convert_alpha()


        for row_index, row in enumerate(TUTORIAL_LAYOUT):
            for col_index, tile_code in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if tile_code == 'W':
                    Tile(self.parede_tile_img, x, y, groups=[self.background_group])
                    self.add_object("parede", 0, x, y)
                
                elif tile_code == 'P':
                    Tile(self.chao_tile_img, x, y, groups=[self.background_group])
                    self.player.rect.topleft = (x, y)
                
                elif tile_code == 'E':
                    Tile(self.chao_tile_img, x, y, groups=[self.background_group])
                    self.add_enemy(0, 0, x, y)

                elif tile_code == ' ':
                    Tile(self.chao_tile_img, x, y, groups=[self.background_group])
