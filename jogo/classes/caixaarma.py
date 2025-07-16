from classes.game_object import*
from utils.funcoes import*

class CaixaArma(GameObject):
    def __init__(self, screen, x, y, tipo_arma):
        # Supondo que você tenha um sprite para a caixa de arma
        super().__init__(screen, "jogo/sprites/caixa_fechada.png", x, y)

        self.hitbox = self.rect.inflate(-10, -10)
        
        self.tipo_arma = tipo_arma
        self.usada = False # Controla se a caixa já foi aberta
        
        # Sprites para os estados da caixa
        self.sprite_fechada = self.image
        self.sprite_aberta = carregar_imagem("jogo/sprites/caixa_aberta.png")
    
    def abrir(self):
        if not self.usada:
            self.usada = True
            self.image = self.sprite_aberta