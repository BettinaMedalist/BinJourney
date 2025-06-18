from classes.fase import*

class Tutorial(Fase):
    def __init__(self, screen, image_path, player, delta_time):
        super().__init__(screen, image_path, player, delta_time)
        self.add_enemy(0 ,1, 1)
    
    def running(self):
        self.update()