from classes.inimigo import*
from classes.parede import*

class Fase(GameObject):
    def __init__(self, screen, image_path, player, delta_time):
        super().__init__(screen, image_path)
        self.enemies = []
        self.objects = []
        self.delta_time = delta_time
        self.player = player

    def add_enemy(self, enemy_type, angle, x, y):
        self.enemies.append(Inimigo_Pistola(self.screen, angle, x, y))

    def add_object(self, object_type, angle, x, y):
        if object_type == "parede":
            self.objects.append(Parede(self.screen, x, y))


    def movement(self, player):
        self.rect.x += (player.left - player.right) * self.delta_time * player.running
        self.rect.y += (player.up - player.down) * self.delta_time * player.running
        for objeto in self.objects:
            objeto.rect.x += (player.left - player.right) * self.delta_time * player.running
            objeto.rect.y += (player.up - player.down) * self.delta_time * player.running
        for inimigo in self.enemies:
            inimigo.rect.x += (player.left - player.right) * self.delta_time * player.running
            inimigo.rect.y += (player.up - player.down) * self.delta_time * player.running
        for bala in player.shots:
            bala.rect.x += (player.left - player.right) * self.delta_time * player.running
            bala.rect.y += (player.up - player.down) * self.delta_time * player.running
    
    def update(self):
        for bala in self.player.shots:
            for inimigo in self.enemies:
            
                if inimigo.rect.colliderect(bala):
                    inimigo.vidas -= 1
                    self.player.shots.remove(bala)
                if inimigo and inimigo.vidas <= 0:
                    self.enemies.remove(inimigo)

    def render(self):
        self.draw()
        for inimigo in self.enemies:
            inimigo.draw()
        for objeto in self.objects:
            objeto.draw()

    def running(self):
        self.update()