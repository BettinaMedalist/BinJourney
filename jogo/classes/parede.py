# Arquivo: parede.py (Versão Correta)

from classes.game_object import*

class Parede(GameObject):
    def __init__(self, screen, x, y):
        # Caminho do arquivo corrigido
        super().__init__(screen, "jogo/sprites/parede.png", x, y)