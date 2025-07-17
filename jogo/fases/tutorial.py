from classes.fase import Fase
from constantes import *

# A matriz do layout define a estrutura do nível
TUTORIAL_LAYOUT = [
    'WWWWWWWWWWWWWWWWWWWWWWW',
    'W                     W',
    'W                     W',
    'W          G          W', # G = Inimigo Pistola
    'W                     W',
    'W         J           W', # J = Jogador
    'W                     W',
    'W                     W',
    'WWWWWWWWWWWWWWWWWWWWWWW',
]
TILE_SIZE = 64


class Tutorial(Fase):
    def __init__(self, screen, player):
        # 1. Inicializa a classe Fase base
        super().__init__(screen, player)

        # 2. Chama o método para construir o nível usando o layout e o tamanho do tile
        self.create_level(TUTORIAL_LAYOUT, TILE_SIZE)