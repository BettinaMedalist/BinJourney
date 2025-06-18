from classes.game_object import*

#Não sei se vale a pena fazer uma classe botão
class Botao(GameObject):
    def __init__(self, screen, image_path):
        super().__init__(screen, image_path)

    def apertado(self):
        m_pos = pygame.mouse.get_pos()
        mouse_button = pygame.mouse.get_pressed()
        if self.rect.collidepoint(m_pos) and mouse_button[0]:
            return True
        return False