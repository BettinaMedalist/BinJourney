# Arquivo: fase1.py (Versão Correta)

from classes.fase import*

class Fase1(Fase):
    # 'delta_time' removido daqui
    def __init__(self, screen, player):
        # 'delta_time' removido daqui e caminho do arquivo corrigido
        super().__init__(screen, "jogo/sprites/paredes.png", player)