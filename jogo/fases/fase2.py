from classes.fase import Fase
<<<<<<< Updated upstream
<<<<<<< Updated upstream
from constantes import *

LAYOUT_FASE2 = [
'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
'W                                            W',
'W   P                                   P    W',
'W                                            W',
'W        WWWWWWWWWWWWWWWWWWWWWWWWWWWW        W',
'W        W                         WW        W',
'W        W   M     M      M   M    WW        W',
'W        W                         WW        W',
'W        W   M         K       M   WW        W',
'W        W                         WW        W',
'W        WWWWWWWWWWW      WWWWWWWWWWW        W',
'W                                            W',
'W                                       P    W',
'W                                            W',
'W        WWWWWWWWWWWW     WWWWWWWWWWW        W',
'W        W                          W        W',
'W        W                          W        W',
'W    J   W     G      M        G    W L      W',
'W        W                          W        W',
'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
]

TILE_SIZE = 64


class Fase2(Fase):
    def __init__(self, screen, player):
        # 1. Inicializa a classe Fase base
        super().__init__(screen, player)

        # 2. Chama o método para construir o nível usando o layout e o tamanho do tile
        self.create_level(LAYOUT_FASE2, TILE_SIZE)
=======
from constantes import *
>>>>>>> Stashed changes
=======
from constantes import *
>>>>>>> Stashed changes
